#!/usr/bin/env python3
"""
Script to compare Rust RocksDB API with C++ RocksDB API
and identify missing features.
"""

import re
import subprocess
from pathlib import Path

def extract_rust_public_methods():
    """Extract public methods from Rust codebase."""
    methods = set()
    
    # Extract from db.rs
    db_rs = Path("/workspace/src/db.rs").read_text()
    # Match pub fn patterns
    for match in re.finditer(r'pub fn (\w+)', db_rs):
        methods.add(match.group(1))
    
    # Extract from backup.rs
    backup_rs = Path("/workspace/src/backup.rs").read_text()
    for match in re.finditer(r'pub fn (\w+)', backup_rs):
        methods.add(f"backup_{match.group(1)}")
    
    # Extract from checkpoint.rs
    checkpoint_rs = Path("/workspace/src/checkpoint.rs").read_text()
    for match in re.finditer(r'pub fn (\w+)', checkpoint_rs):
        methods.add(f"checkpoint_{match.group(1)}")
    
    return methods

def extract_cpp_public_methods():
    """Extract public methods from C++ RocksDB header."""
    methods = set()
    
    try:
        cpp_header = Path("/tmp/rocksdb_db.h").read_text()
    except:
        print("Warning: Could not read C++ header file")
        return methods
    
    # Match virtual Status methods
    for match in re.finditer(r'virtual Status (\w+)', cpp_header):
        methods.add(match.group(1))
    
    # Match static Status methods
    for match in re.finditer(r'static Status (\w+)', cpp_header):
        methods.add(match.group(1))
    
    # Match const methods
    for match in re.finditer(r'virtual (\w+)\(', cpp_header):
        methods.add(match.group(1))
    
    return methods

def normalize_method_name(name):
    """Normalize method names for comparison."""
    # Convert CamelCase to snake_case
    name = re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()
    return name

def map_cpp_to_rust_method(cpp_method):
    """Map C++ method names to likely Rust equivalents."""
    mappings = {
        'open': 'open',
        'open_for_read_only': 'open_for_read_only',
        'open_as_secondary': 'open_as_secondary',
        'create_column_family': 'create_cf',
        'drop_column_family': 'drop_cf',
        'put': 'put',
        'delete': 'delete',
        'merge': 'merge',
        'write': 'write',
        'get': 'get',
        'multi_get': 'multi_get',
        'new_iterator': 'iterator',
        'get_snapshot': 'snapshot',
        'compact_range': 'compact_range',
        'flush': 'flush',
        'flush_wal': 'flush_wal',
        'disable_file_deletions': 'disable_file_deletions',
        'enable_file_deletions': 'enable_file_deletions',
        'list_column_families': 'list_cf',
        'destroy': 'destroy',
        'repair': 'repair',
        'ingest_external_file': 'ingest_external_file',
        'get_property': 'property_value',
        'get_int_property': 'property_int_value',
        'get_approximate_sizes': 'get_approximate_sizes',
        'set_options': 'set_options',
        'wait_for_compact': 'wait_for_compact',
        'get_updates_since': 'get_updates_since',
        'try_catch_up_with_primary': 'try_catch_up_with_primary',
        'key_may_exist': 'key_may_exist',
        'get_latest_sequence_number': 'latest_sequence_number',
    }
    
    normalized = normalize_method_name(cpp_method)
    return mappings.get(normalized, normalized)

def find_missing_features():
    """Find missing features by comparing APIs."""
    rust_methods = extract_rust_public_methods()
    cpp_methods = extract_cpp_public_methods()
    
    print("=" * 80)
    print("RocksDB API Comparison Analysis")
    print("=" * 80)
    
    # Key C++ methods to check
    key_cpp_methods = [
        'Open', 'OpenForReadOnly', 'OpenAsSecondary', 'OpenAsFollower',
        'OpenAndCompact', 'OpenAndTrimHistory',
        'CreateColumnFamily', 'CreateColumnFamilies', 'DropColumnFamily', 'DropColumnFamilies',
        'DestroyColumnFamilyHandle',
        'Put', 'PutEntity', 'Delete', 'SingleDelete', 'DeleteRange', 'Merge',
        'Write', 'WriteWithCallback', 'IngestWriteBatchWithIndex',
        'Get', 'GetEntity', 'GetMergeOperands', 'MultiGet', 'MultiGetEntity',
        'KeyMayExist',
        'NewIterator', 'NewIterators', 'NewCoalescingIterator', 
        'NewAttributeGroupIterator', 'NewMultiScan',
        'GetSnapshot', 'ReleaseSnapshot',
        'GetProperty', 'GetMapProperty', 'GetIntProperty', 'GetAggregatedIntProperty',
        'ResetStats',
        'GetApproximateSizes', 'GetApproximateMemTableStats',
        'CompactRange', 'CompactFiles',
        'SetOptions', 'SetDBOptions',
        'PauseBackgroundWork', 'ContinueBackgroundWork',
        'EnableAutoCompaction',
        'DisableManualCompaction', 'EnableManualCompaction',
        'WaitForCompact',
        'NumberLevels', 'MaxMemCompactionLevel', 'Level0StopWriteTrigger',
        'GetName', 'GetEnv', 'GetFileSystem', 'GetOptions', 'GetDBOptions',
        'Flush', 'FlushWAL', 'SyncWAL', 'LockWAL', 'UnlockWAL',
        'GetLatestSequenceNumber',
        'IncreaseFullHistoryTsLow', 'GetFullHistoryTsLow', 'GetNewestUserDefinedTimestamp',
        'DisableFileDeletions', 'EnableFileDeletions',
        'GetCreationTimeOfOldestFile',
        'GetUpdatesSince',
        'Resume', 'Close',
        'ListColumnFamilies',
    ]
    
    missing_features = []
    implemented_features = []
    
    for cpp_method in key_cpp_methods:
        normalized = normalize_method_name(cpp_method)
        rust_equiv = map_cpp_to_rust_method(cpp_method)
        
        # Check if implemented (exact match or partial match)
        found = False
        for rust_method in rust_methods:
            if rust_equiv in rust_method or rust_method in rust_equiv:
                found = True
                break
            # Also check for cf variants
            if f"{rust_equiv}_cf" in rust_method or f"{rust_equiv}_opt" in rust_method:
                found = True
                break
        
        if found:
            implemented_features.append(cpp_method)
        else:
            missing_features.append((cpp_method, rust_equiv))
    
    print(f"\nImplemented Features: {len(implemented_features)}")
    print(f"Missing Features: {len(missing_features)}")
    
    print("\n" + "=" * 80)
    print("MISSING FEATURES:")
    print("=" * 80)
    
    # Group missing features by category
    categories = {
        'Open/Close': [],
        'Column Family Management': [],
        'Write Operations': [],
        'Read Operations': [],
        'Iterator Operations': [],
        'Properties/Stats': [],
        'Compaction': [],
        'Background Work': [],
        'File Management': [],
        'Time Series': [],
        'Advanced Features': [],
    }
    
    for cpp_method, rust_equiv in missing_features:
        if 'Open' in cpp_method or 'Close' in cpp_method or 'Resume' in cpp_method:
            categories['Open/Close'].append((cpp_method, rust_equiv))
        elif 'ColumnFamily' in cpp_method or 'CF' in cpp_method:
            categories['Column Family Management'].append((cpp_method, rust_equiv))
        elif 'Put' in cpp_method or 'Delete' in cpp_method or 'Merge' in cpp_method or 'Write' in cpp_method:
            categories['Write Operations'].append((cpp_method, rust_equiv))
        elif 'Get' in cpp_method or 'KeyMayExist' in cpp_method:
            categories['Read Operations'].append((cpp_method, rust_equiv))
        elif 'Iterator' in cpp_method or 'Scan' in cpp_method:
            categories['Iterator Operations'].append((cpp_method, rust_equiv))
        elif 'Property' in cpp_method or 'Stats' in cpp_method or 'Approximate' in cpp_method:
            categories['Properties/Stats'].append((cpp_method, rust_equiv))
        elif 'Compact' in cpp_method:
            categories['Compaction'].append((cpp_method, rust_equiv))
        elif 'Background' in cpp_method or 'Pause' in cpp_method or 'Continue' in cpp_method:
            categories['Background Work'].append((cpp_method, rust_equiv))
        elif 'File' in cpp_method:
            categories['File Management'].append((cpp_method, rust_equiv))
        elif 'Timestamp' in cpp_method or 'History' in cpp_method or 'TS' in cpp_method:
            categories['Time Series'].append((cpp_method, rust_equiv))
        else:
            categories['Advanced Features'].append((cpp_method, rust_equiv))
    
    for category, features in categories.items():
        if features:
            print(f"\n### {category} ({len(features)} missing)")
            for cpp_method, rust_equiv in sorted(features):
                print(f"  - {cpp_method} (expected Rust equivalent: {rust_equiv})")
    
    return missing_features

if __name__ == "__main__":
    missing = find_missing_features()
    print(f"\n\nTotal missing features: {len(missing)}")
