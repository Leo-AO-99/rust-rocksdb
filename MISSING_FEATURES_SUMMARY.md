# RocksDB Rust 版本缺失功能总结

本文档总结了 Rust RocksDB 包装器与 C++ RocksDB 官方版本相比缺失的主要功能。

## 快速参考

### 高优先级缺失功能（17个）

1. **SingleDelete** - 单次删除操作（用于删除操作只执行一次的场景）
2. **SyncWAL** - 同步 WAL 到磁盘
3. **PauseBackgroundWork / ContinueBackgroundWork** - 后台工作控制
4. **CompactFiles** - 压缩指定文件
5. **EnableAutoCompaction / DisableManualCompaction / EnableManualCompaction** - 压缩控制
6. **SetDBOptions / GetDBOptions / GetOptions** - 选项管理
7. **ResetStats** - 重置统计信息
8. **Close / Resume** - 显式关闭/恢复数据库
9. **CreateColumnFamilies / DropColumnFamilies** - 批量列族操作
10. **GetMergeOperands** - 获取合并操作数
11. **NewIterators** - 为多个列族创建迭代器
12. **GetApproximateMemTableStats** - 获取 MemTable 统计
13. **GetCreationTimeOfOldestFile** - 获取最老文件创建时间
14. **LockWAL / UnlockWAL** - WAL 锁定/解锁
15. **GetSortedWalFiles / GetCurrentWalFile** - WAL 文件管理
16. **GetAggregatedIntProperty** - 获取聚合整数属性
17. **NumberLevels / MaxMemCompactionLevel / Level0StopWriteTrigger** - 数据库级别信息

### 中优先级缺失功能（10个）

1. **Wide Columns 支持** - PutEntity, GetEntity, MultiGetEntity, NewAttributeGroupIterator
2. **OpenAsFollower** - 作为跟随者打开
3. **OpenAndCompact / OpenAndTrimHistory** - 打开时压缩/修剪
4. **NewCoalescingIterator / NewMultiScan** - 高级迭代器
5. **WriteWithCallback** - 带回调写入
6. **IngestWriteBatchWithIndex** - 导入带索引批次
7. **IngestExternalFiles** - 批量导入外部文件
8. **GetLiveFilesChecksumInfo / GetLiveFilesStorageInfo** - 文件信息查询
9. **GetNewestUserDefinedTimestamp** - 获取最新时间戳
10. **CreateColumnFamilyWithImport** - 通过导入创建列族

## 详细分类

### 1. 写入操作缺失
- SingleDelete / SingleDeleteCF
- PutEntity / PutEntityCF (Wide Columns)
- WriteWithCallback
- IngestWriteBatchWithIndex

### 2. 读取操作缺失
- GetEntity / GetEntityCF (Wide Columns)
- MultiGetEntity
- GetMergeOperands

### 3. 迭代器缺失
- NewIterators (多列族迭代器)
- NewCoalescingIterator
- NewAttributeGroupIterator (Wide Columns)
- NewMultiScan

### 4. 压缩操作缺失
- CompactFiles / CompactFilesCF
- EnableAutoCompaction
- DisableManualCompaction / EnableManualCompaction

### 5. 后台工作控制缺失
- PauseBackgroundWork
- ContinueBackgroundWork

### 6. WAL 操作缺失
- SyncWAL
- LockWAL / UnlockWAL
- GetSortedWalFiles / GetCurrentWalFile

### 7. 选项管理缺失
- SetDBOptions
- GetDBOptions / GetOptions

### 8. 统计信息缺失
- ResetStats
- GetApproximateMemTableStats
- GetAggregatedIntProperty
- GetCreationTimeOfOldestFile

### 9. 数据库信息缺失
- NumberLevels
- MaxMemCompactionLevel
- Level0StopWriteTrigger
- GetNewestUserDefinedTimestamp

### 10. 列族管理缺失
- CreateColumnFamilies
- DropColumnFamilies
- CreateColumnFamilyWithImport

### 11. 数据库打开/关闭缺失
- OpenAsFollower
- OpenAndCompact / OpenAndTrimHistory
- Resume / Close

## 实现建议

### 第一阶段：基础常用功能（易实现）
这些功能在 C API 中已经可用，只需要在 Rust 层包装：

1. **SingleDelete** - `rocksdb_singledelete` 已可用
2. **SyncWAL** - 需要确认 C API
3. **PauseBackgroundWork / ContinueBackgroundWork** - 需要确认 C API
4. **CompactFiles** - 需要确认 C API
5. **EnableAutoCompaction / DisableManualCompaction / EnableManualCompaction** - 部分已确认
6. **ResetStats** - 需要确认 C API
7. **Close** - `rocksdb_close` 已可用
8. **NewIterators** - `rocksdb_create_iterators` 已可用

### 第二阶段：选项和统计功能
1. **SetDBOptions / GetDBOptions / GetOptions** - 需要确认 C API
2. **GetApproximateMemTableStats** - 需要确认 C API
3. **GetAggregatedIntProperty** - 需要确认 C API
4. **GetCreationTimeOfOldestFile** - 需要确认 C API
5. **NumberLevels / MaxMemCompactionLevel / Level0StopWriteTrigger** - 需要确认 C API

### 第三阶段：批量操作和 WAL 功能
1. **CreateColumnFamilies / DropColumnFamilies** - 需要确认 C API
2. **GetMergeOperands** - 需要确认 C API
3. **LockWAL / UnlockWAL** - 需要确认 C API
4. **GetSortedWalFiles / GetCurrentWalFile** - 需要确认 C API

### 第四阶段：新特性和高级功能
1. **Wide Columns 支持** - 需要检查 RocksDB 版本和 C API 支持
2. **OpenAsFollower** - 需要检查 C API
3. **OpenAndCompact / OpenAndTrimHistory** - 需要检查 C API
4. **其他高级迭代器** - 需要检查 C API

## 检查清单

在实现功能前，建议：

1. ✅ 检查 `librocksdb-sys` 中的 FFI 绑定，确认底层函数是否可用
2. ✅ 检查 RocksDB 版本要求
3. ✅ 查看 C API 文档 (`c.h`) 确认函数签名
4. ✅ 参考 C++ API 文档 (`db.h`) 了解功能用途
5. ✅ 添加适当的错误处理
6. ✅ 添加单元测试和集成测试
7. ✅ 更新文档

## 相关文件

- 详细报告：`missing_features_report.md`
- 对比脚本：`compare_api.py`
- RocksDB C++ API: https://github.com/facebook/rocksdb/blob/main/include/rocksdb/db.h
- RocksDB C API: https://github.com/facebook/rocksdb/blob/main/include/rocksdb/c.h

## 贡献指南

如果你想要实现某个缺失功能：

1. 查看 `missing_features_report.md` 了解详细说明
2. 检查底层 FFI 是否可用
3. 参考现有实现（如 `SingleDelete` 参考 `Delete`）
4. 实现功能并添加测试
5. 提交 Pull Request
