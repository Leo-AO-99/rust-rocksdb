# RocksDB Rust 绑定缺失功能对比

本文档对比了 C++ 版本的 RocksDB (https://github.com/facebook/rocksdb) 和当前 Rust 绑定的功能差异，列出了缺失的功能。

## 核心 DB 操作

### 1. SingleDelete 操作
- **C++ API**: `Status SingleDelete(const WriteOptions&, ColumnFamilyHandle*, const Slice&)`
- **C API**: ✅ 已存在 `rocksdb_writebatch_singledelete`, `rocksdb_writebatch_singledelete_cf`
- **状态**: ❌ 未实现
- **说明**: SingleDelete 用于删除只写入一次（没有重复写入）的键，比 Delete 更高效。适用于明确知道某个键只被写入一次的场景。
- **实现难度**: 🟢 低（C API 已存在）

### 2. GetMergeOperands
- **C++ API**: `Status GetMergeOperands(const ReadOptions&, ColumnFamilyHandle*, const Slice&, ...)`
- **状态**: ❌ 未实现
- **说明**: 获取某个键的所有合并操作数（merge operands），用于自定义合并逻辑。

### 3. NewIterators
- **C++ API**: `Status NewIterators(const ReadOptions&, const std::vector<ColumnFamilyHandle*>&, std::vector<Iterator*>* out_iterators)`
- **状态**: ❌ 未实现
- **说明**: 为多个列族创建多个迭代器，可以原子性地获取多个列族的快照视图。

## WAL (Write-Ahead Log) 操作

### 4. SyncWAL
- **C++ API**: `Status SyncWAL()`
- **状态**: ❌ 未实现
- **说明**: 同步 WAL 到磁盘，确保所有已提交的写入都持久化。

### 5. LockWAL / UnlockWAL
- **C++ API**: `Status LockWAL()` / `Status UnlockWAL()`
- **状态**: ❌ 未实现
- **说明**: 锁定/解锁 WAL，用于在备份期间防止 WAL 被删除。

### 6. GetSortedWalFiles
- **C++ API**: `Status GetSortedWalFiles(VectorLogPtr& files)`
- **状态**: ❌ 未实现
- **说明**: 获取排序后的 WAL 文件列表，用于备份和恢复。

### 7. GetCurrentWalFile
- **C++ API**: `Status GetCurrentWalFile(std::unique_ptr<LogFile>* current_log_file)`
- **状态**: ❌ 未实现
- **说明**: 获取当前正在使用的 WAL 文件信息。

## 后台任务控制

### 8. PauseBackgroundWork / ContinueBackgroundWork
- **C++ API**: `Status PauseBackgroundWork()` / `Status ContinueBackgroundWork()`
- **状态**: ❌ 未实现
- **说明**: 暂停/恢复后台任务（压缩、刷新等），用于性能测试或特定场景下的性能控制。

### 9. EnableAutoCompaction
- **C++ API**: `Status EnableAutoCompaction(const std::vector<ColumnFamilyHandle*>& column_families)`
- **状态**: ❌ 未实现
- **说明**: 启用特定列族的自动压缩。

## 压缩操作

### 10. CompactFiles
- **C++ API**: `Status CompactFiles(const CompactionOptions&, ColumnFamilyHandle*, const std::vector<std::string>&, int output_level, ...)`
- **状态**: ❌ 未实现
- **说明**: 压缩指定的文件列表，允许更精细的压缩控制。

### 11. GetApproximateSizes (带 SizeApproximationOptions)
- **C++ API**: `Status GetApproximateSizes(const SizeApproximationOptions&, ColumnFamilyHandle*, const Range*, int, uint64_t*)`
- **状态**: ⚠️ 部分实现
- **说明**: 当前有 `get_approximate_sizes`，但缺少带 `SizeApproximationOptions` 参数的版本，无法控制估算的精度。

## 文件操作

### 12. DeleteFile
- **C++ API**: `Status DeleteFile(std::string name)`
- **C API**: ✅ 已存在 `rocksdb_delete_file`
- **状态**: ❌ 未实现
- **说明**: 删除指定的文件，通常用于手动管理 SST 文件。
- **实现难度**: 🟢 低（C API 已存在）

### 13. GetLiveFilesChecksumInfo
- **C++ API**: `Status GetLiveFilesChecksumInfo(FileChecksumList* checksum_list)`
- **状态**: ❌ 未实现
- **说明**: 获取所有活动文件的校验和信息，用于数据完整性验证。

### 14. GetCreationTimeOfOldestFile
- **C++ API**: `Status GetCreationTimeOfOldestFile(uint64_t* creation_time)`
- **状态**: ❌ 未实现
- **说明**: 获取最旧文件的创建时间，用于监控和清理策略。

## 数据完整性验证

### 15. VerifyChecksum
- **C++ API**: `Status VerifyChecksum(const ReadOptions& read_options)` / `Status VerifyChecksum()`
- **C API**: ⚠️ 部分存在（`rocksdb_readoptions_set_verify_checksums` 用于 ReadOptions，但可能缺少 DB 级别的验证方法）
- **状态**: ❌ 未实现
- **说明**: 验证数据库的校验和，用于数据完整性检查。
- **实现难度**: 🟡 中（需要确认 C API 的完整支持）

### 16. VerifyFileChecksums
- **C++ API**: `Status VerifyFileChecksums(const ReadOptions& read_options)`
- **状态**: ❌ 未实现
- **说明**: 验证所有文件的校验和。

## 列族操作

### 17. DropColumnFamilies (批量)
- **C++ API**: `Status DropColumnFamilies(const std::vector<ColumnFamilyHandle*>&)`
- **状态**: ⚠️ 部分实现
- **说明**: 当前只有单个列族的 `drop_cf`，缺少批量删除的版本。

### 18. DestroyColumnFamilyHandle
- **C++ API**: `Status DestroyColumnFamilyHandle(ColumnFamilyHandle* column_family)`
- **状态**: ❌ 未实现
- **说明**: 显式销毁列族句柄，释放资源。

### 19. GetDescriptor (ColumnFamilyHandle)
- **C++ API**: `Status GetDescriptor(ColumnFamilyDescriptor* desc)`
- **状态**: ❌ 未实现
- **说明**: 获取列族的描述符（选项配置）。

### 20. CreateColumnFamilyWithImport
- **C++ API**: `Status CreateColumnFamilyWithImport(const ColumnFamilyOptions&, const std::string&, const ImportColumnFamilyOptions&, ...)`
- **状态**: ❌ 未实现
- **说明**: 通过导入 SST 文件创建列族。

## 数据库元数据

### 21. GetDbSessionId
- **C++ API**: `Status GetDbSessionId(std::string& session_id) const`
- **状态**: ❌ 未实现
- **说明**: 获取数据库会话 ID，用于跟踪和调试。

### 22. ResetStats
- **C++ API**: `Status ResetStats()`
- **状态**: ❌ 未实现
- **说明**: 重置统计信息。

## 外部文件操作

### 23. IngestExternalFiles (批量)
- **C++ API**: `Status IngestExternalFiles(const std::vector<IngestExternalFileArg>&)`
- **状态**: ⚠️ 部分实现
- **说明**: 当前有单个列族的 `ingest_external_file`，缺少批量操作的版本。

## 事件监听

### 24. EventListener
- **C++ API**: `void SetEventListener(EventListener*)` 及相关事件回调
- **状态**: ❌ 未实现
- **说明**: 事件监听器，用于监听数据库事件（压缩、刷新、错误等）。这是一个重要的功能，用于监控和调试。

### 25. EventListener 相关事件
- **状态**: ❌ 未实现
- **包括**:
  - OnFlushCompleted
  - OnCompactionCompleted
  - OnTableFileCreated
  - OnTableFileDeleted
  - OnMemTableSealed
  - OnColumnFamilyHandleDeletionStarted
  - OnExternalFileIngested
  - OnBackgroundError
  - OnStallConditionsChanged
  - OnFileReadFinish
  - OnFileWriteFinish
  - OnFileFlushFinish
  - OnFileSyncFinish
  - OnFileRangeSyncFinish
  - OnFileTruncateFinish
  - OnFileCloseFinish
  - OnFilePrefetchFinish

## Options 相关

### 26. 一些 Options 设置方法可能缺失
- **状态**: ⚠️ 需要详细检查
- **说明**: C++ RocksDB 有大量的 Options 设置方法，需要逐一对比确认是否都已暴露。

## 事务相关

### 27. Transaction 的一些高级功能
- **状态**: ⚠️ 需要详细检查
- **说明**: 需要对比 C++ Transaction API 和 Rust 绑定，确认是否有高级功能缺失。

## WriteBatch 相关

### 28. WriteBatch::SingleDelete
- **C++ API**: `void SingleDelete(ColumnFamilyHandle*, const Slice&)`
- **C API**: ✅ 已存在 `rocksdb_writebatch_singledelete`, `rocksdb_writebatch_singledelete_cf`
- **状态**: ❌ 未实现
- **说明**: WriteBatch 中的 SingleDelete 操作。
- **实现难度**: 🟢 低（C API 已存在）

### 29. WriteBatch::GetWriteBatch
- **状态**: ⚠️ 需要确认
- **说明**: 获取 WriteBatch 的内部表示。

## 其他功能

### 30. 线程状态监控
- **C++ API**: `GetThreadList()` 及相关类型
- **状态**: ❌ 未实现
- **说明**: 获取线程状态信息，用于监控和调试。

### 31. 统计历史记录
- **C++ API**: `StatsHistoryIterator` 及相关方法
- **状态**: ❌ 未实现
- **说明**: 获取统计信息的历史记录。

### 32. 跟踪和追踪
- **C++ API**: `TraceWriter`, `TraceReader` 及相关方法
- **状态**: ❌ 未实现
- **说明**: 用于跟踪和重放数据库操作。

## 优先级建议

### 高优先级（核心功能）
1. **SingleDelete** - 重要的删除操作优化
2. **SyncWAL** - 数据持久化保证
3. **GetMergeOperands** - 合并操作支持
4. **VerifyChecksum** - 数据完整性验证
5. **EventListener** - 监控和调试支持

### 中优先级（实用功能）
6. **PauseBackgroundWork / ContinueBackgroundWork** - 性能控制
7. **CompactFiles** - 精细压缩控制
8. **GetDbSessionId** - 调试支持
9. **NewIterators** - 多列族原子视图
10. **WAL 相关操作** - 备份和恢复支持

### 低优先级（高级功能）
11. **线程状态监控** - 高级调试
12. **统计历史记录** - 性能分析
13. **跟踪和追踪** - 高级调试

## C API (FFI) 可用性说明

某些功能可能在 C++ API 中存在，但在 C API (FFI) 中不可用。在实现这些功能之前，需要：

1. 检查 C API 头文件 (`rocksdb/c.h`) 是否包含相应的函数
2. 如果 C API 中没有，可能需要：
   - 在 C++ RocksDB 中添加 C API 包装
   - 或者直接在 Rust 中通过 FFI 调用 C++ API（需要额外的绑定工作）

## 注意事项

1. 本文档基于 C++ RocksDB 的最新版本（master 分支）对比
2. 某些功能可能因为 FFI 绑定的限制而难以实现
3. 某些功能可能需要在底层 C API (librocksdb-sys) 中先实现
4. 建议在实现新功能时，参考 C++ RocksDB 的文档和测试用例
5. 在实现之前，请先检查 C API 的可用性

## 贡献指南

如果您想贡献这些缺失的功能，建议：
1. 先查看 C++ RocksDB 的源代码和文档
2. 检查 FFI 绑定是否已经存在对应的 C API
3. 如果没有，可能需要先在 `librocksdb-sys` 中添加 FFI 绑定
4. 参考现有功能的实现模式
5. 添加相应的测试用例
