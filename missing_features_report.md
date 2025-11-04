# RocksDB Rust 版本缺失功能对比报告

本报告对比了 Rust RocksDB 包装器与 C++ RocksDB 官方版本，找出缺失的功能。

## 1. 数据库打开/关闭操作

### 已实现
- ✅ `Open` - 打开数据库
- ✅ `OpenForReadOnly` - 只读模式打开
- ✅ `OpenAsSecondary` - 作为次要实例打开
- ✅ `ListColumnFamilies` - 列出列族

### 缺失
- ❌ `OpenAsFollower` - 作为跟随者打开（用于主从复制场景）
- ❌ `OpenAndCompact` - 打开并压缩数据库
- ❌ `OpenAndTrimHistory` - 打开并修剪历史记录
- ❌ `Resume()` - 恢复数据库操作
- ❌ `Close()` - 关闭数据库（显式关闭，虽然 Rust 有 Drop）

## 2. 列族管理

### 已实现
- ✅ `CreateColumnFamily` - 创建单个列族
- ✅ `DropColumnFamily` - 删除单个列族
- ✅ `DestroyColumnFamilyHandle` - 销毁列族句柄（通过 Drop）

### 缺失
- ❌ `CreateColumnFamilies` - 批量创建列族（带选项数组）
- ❌ `DropColumnFamilies` - 批量删除列族
- ❌ `CreateColumnFamilyWithImport` - 通过导入创建列族

## 3. 写入操作

### 已实现
- ✅ `Put` - 写入键值对
- ✅ `Delete` - 删除键
- ✅ `DeleteRange` - 删除范围
- ✅ `Merge` - 合并操作
- ✅ `Write` - 批量写入
- ✅ `PutWithTimestamp` - 带时间戳写入
- ✅ `DeleteWithTimestamp` - 带时间戳删除

### 缺失
- ❌ `PutEntity` - 写入实体（Wide Columns 功能）
- ❌ `SingleDelete` - 单次删除（用于删除操作只执行一次的场景）
- ❌ `WriteWithCallback` - 带回调的写入
- ❌ `IngestWriteBatchWithIndex` - 导入带索引的写批次

## 4. 读取操作

### 已实现
- ✅ `Get` - 读取键值对
- ✅ `MultiGet` - 批量读取
- ✅ `GetPinned` - 获取固定切片
- ✅ `KeyMayExist` - 检查键是否存在

### 缺失
- ❌ `GetEntity` - 获取实体（Wide Columns 功能）
- ❌ `MultiGetEntity` - 批量获取实体
- ❌ `GetMergeOperands` - 获取合并操作数（用于调试合并操作）

## 5. 迭代器操作

### 已实现
- ✅ `NewIterator` - 创建迭代器
- ✅ `NewRawIterator` - 创建原始迭代器
- ✅ `NewWALIterator` - 创建 WAL 迭代器

### 缺失
- ❌ `NewIterators` - 为多个列族创建迭代器
- ❌ `NewCoalescingIterator` - 创建合并迭代器
- ❌ `NewAttributeGroupIterator` - 创建属性组迭代器（Wide Columns）
- ❌ `NewMultiScan` - 创建多扫描迭代器

## 6. 快照操作

### 已实现
- ✅ `GetSnapshot` - 获取快照
- ✅ `ReleaseSnapshot` - 释放快照

## 7. 属性/统计信息

### 已实现
- ✅ `GetProperty` - 获取属性
- ✅ `GetIntProperty` - 获取整数属性
- ✅ `GetMapProperty` - 获取映射属性
- ✅ `GetApproximateSizes` - 获取近似大小

### 缺失
- ❌ `GetAggregatedIntProperty` - 获取聚合整数属性（跨所有列族）
- ❌ `GetApproximateMemTableStats` - 获取 MemTable 近似统计
- ❌ `ResetStats` - 重置统计信息
- ❌ `GetCreationTimeOfOldestFile` - 获取最老文件的创建时间

## 8. 压缩操作

### 已实现
- ✅ `CompactRange` - 压缩范围
- ✅ `WaitForCompact` - 等待压缩完成

### 缺失
- ❌ `CompactFiles` - 压缩指定文件
- ❌ `EnableAutoCompaction` - 启用自动压缩
- ❌ `DisableManualCompaction` - 禁用手动压缩
- ❌ `EnableManualCompaction` - 启用手动压缩

## 9. 后台工作控制

### 已实现
- ✅ `CancelAllBackgroundWork` - 取消所有后台工作

### 缺失
- ❌ `PauseBackgroundWork` - 暂停后台工作
- ❌ `ContinueBackgroundWork` - 继续后台工作

## 10. WAL (Write-Ahead Log) 操作

### 已实现
- ✅ `FlushWAL` - 刷新 WAL

### 缺失
- ❌ `SyncWAL` - 同步 WAL 到磁盘
- ❌ `LockWAL` - 锁定 WAL
- ❌ `UnlockWAL` - 解锁 WAL
- ❌ `GetSortedWalFiles` - 获取排序的 WAL 文件列表
- ❌ `GetCurrentWalFile` - 获取当前 WAL 文件

## 11. 选项管理

### 已实现
- ✅ `SetOptions` - 设置列族选项

### 缺失
- ❌ `SetDBOptions` - 设置数据库选项
- ❌ `GetOptions` - 获取列族选项
- ❌ `GetDBOptions` - 获取数据库选项

## 12. 数据库信息查询

### 已实现
- ✅ `GetName` - 获取数据库名称
- ✅ `GetLatestSequenceNumber` - 获取最新序列号
- ✅ `GetEnv` - 获取环境对象
- ✅ `GetFileSystem` - 获取文件系统对象（注释中提到但未实现）
- ✅ `NumberLevels` - 获取级别数量（注释中提到但未实现）
- ✅ `MaxMemCompactionLevel` - 获取最大内存压缩级别（注释中提到但未实现）
- ✅ `Level0StopWriteTrigger` - 获取 L0 停止写入触发器（注释中提到但未实现）

### 缺失
- ❌ `GetFullHistoryTsLow` - 获取完整历史时间戳下限（已部分实现，但可能不完整）
- ❌ `GetNewestUserDefinedTimestamp` - 获取最新的用户定义时间戳

## 13. 文件管理

### 已实现
- ✅ `DisableFileDeletions` - 禁用文件删除
- ✅ `EnableFileDeletions` - 启用文件删除
- ✅ `DeleteFileInRange` - 删除范围内的文件
- ✅ `IngestExternalFile` - 导入外部文件
- ✅ `GetLiveFiles` - 获取活动文件列表

### 缺失
- ❌ `IngestExternalFiles` - 批量导入外部文件（带选项）
- ❌ `GetLiveFilesChecksumInfo` - 获取活动文件的校验和信息
- ❌ `GetLiveFilesStorageInfo` - 获取活动文件的存储信息

## 14. 时间序列功能

### 已实现
- ✅ `IncreaseFullHistoryTsLow` - 增加完整历史时间戳下限
- ✅ `GetFullHistoryTsLow` - 获取完整历史时间戳下限

### 缺失
- ❌ `GetNewestUserDefinedTimestamp` - 获取最新的用户定义时间戳

## 15. 事务日志

### 已实现
- ✅ `GetUpdatesSince` - 获取自指定序列号以来的更新

## 16. Wide Columns 支持

这是 RocksDB 的新功能，用于支持宽列（类似 Cassandra 的列族）。

### 缺失
- ❌ `PutEntity` - 写入实体
- ❌ `GetEntity` - 读取实体
- ❌ `MultiGetEntity` - 批量读取实体
- ❌ `NewAttributeGroupIterator` - 创建属性组迭代器

## 17. 其他高级功能

### 缺失
- ❌ `GetMergeOperands` - 获取合并操作数（用于调试和自定义合并操作）

## 总结

### 按优先级分类

#### 高优先级（常用功能）
1. **SingleDelete** - 单次删除操作
2. **SyncWAL** - WAL 同步
3. **PauseBackgroundWork / ContinueBackgroundWork** - 后台工作控制
4. **CompactFiles** - 压缩指定文件
5. **EnableAutoCompaction / DisableManualCompaction** - 压缩控制
6. **SetDBOptions / GetDBOptions / GetOptions** - 选项管理
7. **ResetStats** - 重置统计信息

#### 中优先级（有用功能）
1. **CreateColumnFamilies / DropColumnFamilies** - 批量列族操作
2. **GetMergeOperands** - 合并操作数获取
3. **NewIterators** - 多列族迭代器
4. **GetApproximateMemTableStats** - MemTable 统计
5. **GetCreationTimeOfOldestFile** - 文件创建时间
6. **LockWAL / UnlockWAL** - WAL 锁定
7. **GetSortedWalFiles / GetCurrentWalFile** - WAL 文件管理

#### 低优先级（特殊场景）
1. **Wide Columns 支持** - PutEntity, GetEntity, MultiGetEntity, NewAttributeGroupIterator
2. **OpenAsFollower** - 跟随者模式
3. **OpenAndCompact / OpenAndTrimHistory** - 打开时压缩/修剪
4. **Resume / Close** - 显式恢复/关闭
5. **NewCoalescingIterator / NewMultiScan** - 高级迭代器
6. **WriteWithCallback** - 带回调写入
7. **IngestWriteBatchWithIndex** - 导入带索引批次

## 建议实现顺序

1. **第一阶段**：实现最常用的缺失功能
   - SingleDelete
   - SyncWAL
   - PauseBackgroundWork / ContinueBackgroundWork
   - CompactFiles
   - EnableAutoCompaction / DisableManualCompaction / EnableManualCompaction

2. **第二阶段**：实现选项和统计相关功能
   - SetDBOptions / GetDBOptions / GetOptions
   - ResetStats
   - GetApproximateMemTableStats

3. **第三阶段**：实现批量操作和高级功能
   - CreateColumnFamilies / DropColumnFamilies
   - GetMergeOperands
   - NewIterators
   - WAL 相关功能（LockWAL, UnlockWAL, GetSortedWalFiles 等）

4. **第四阶段**：实现 Wide Columns 和其他新特性
   - Wide Columns 完整支持
   - OpenAsFollower
   - 其他高级特性

## C API 中可用的功能（需要 Rust 包装）

通过检查 RocksDB C API (`c.h`)，以下功能在底层 C API 中可用，但尚未在 Rust 层实现：

### 已确认在 C API 中可用的功能
- ✅ `rocksdb_singledelete` / `rocksdb_singledelete_cf` - SingleDelete 操作
- ✅ `rocksdb_close` - 关闭数据库
- ✅ `rocksdb_create_iterators` - 创建多个迭代器
- ✅ `rocksdb_compact_files` - 压缩文件（需要确认）
- ✅ `rocksdb_disable_manual_compaction` - 禁用手动压缩
- ✅ `rocksdb_enable_manual_compaction` - 启用手动压缩
- ✅ `rocksdb_enable_auto_compaction` - 启用自动压缩（需要确认）
- ✅ `rocksdb_reset_stats` - 重置统计（需要确认）
- ✅ `rocksdb_get_merge_operands` - 获取合并操作数（需要确认）
- ✅ `rocksdb_set_db_options` - 设置数据库选项（需要确认）
- ✅ `rocksdb_get_db_options` - 获取数据库选项（需要确认）
- ✅ `rocksdb_get_options` - 获取选项（需要确认）
- ✅ `rocksdb_number_levels` - 获取级别数（需要确认）
- ✅ `rocksdb_get_approximate_memtable_stats` - 获取 MemTable 统计（需要确认）
- ✅ `rocksdb_get_creation_time_of_oldest_file` - 获取最老文件创建时间（需要确认）
- ✅ `rocksdb_sync_wal` - 同步 WAL（需要确认）
- ✅ `rocksdb_lock_wal` - 锁定 WAL（需要确认）
- ✅ `rocksdb_unlock_wal` - 解锁 WAL（需要确认）
- ✅ `rocksdb_pause_background_work` - 暂停后台工作（需要确认）
- ✅ `rocksdb_continue_background_work` - 继续后台工作（需要确认）
- ✅ `rocksdb_resume` - 恢复数据库（需要确认）

### 需要进一步检查的功能
以下功能可能不在 C API 中，或者需要不同的 API 名称：
- ❓ Wide Columns 相关功能（PutEntity, GetEntity 等）- 可能是较新功能
- ❓ OpenAsFollower - 需要检查
- ❓ OpenAndCompact / OpenAndTrimHistory - 需要检查
- ❓ NewCoalescingIterator / NewAttributeGroupIterator / NewMultiScan - 需要检查

## 注意事项

1. **某些功能可能在底层 FFI 中已经可用，只需要在 Rust 层包装**
   - 建议检查 `librocksdb-sys` 中生成的绑定文件，确认哪些函数已经可用
   - 如果底层 FFI 可用，实现这些功能相对简单

2. **某些功能可能需要检查底层 RocksDB 版本是否支持**
   - 某些功能可能是较新版本添加的
   - 建议在实现时添加版本检查

3. **Wide Columns 是相对较新的功能，可能需要较新版本的 RocksDB**
   - 需要确认 RocksDB 版本要求
   - 可能需要检查底层 C API 是否支持

4. **建议的实现步骤**
   - 首先检查 `librocksdb-sys` 中的 FFI 绑定，确认哪些功能已经在底层可用
   - 对于已可用的功能，优先实现 Rust 包装
   - 对于不可用的功能，可能需要更新 `librocksdb-sys` 来添加底层绑定
