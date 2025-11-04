# RocksDB Rust 版本缺失功能对比分析

本文档对比了 C++ 版本的 RocksDB 和当前 Rust 版本（rust-rocksdb）的功能，列出了缺失的功能。

## 核心数据库操作

### ✅ 已实现
- ✅ 数据库打开/关闭（`DB::open`, `DB::close`）
- ✅ 基本 CRUD 操作（`put`, `get`, `delete`, `merge`）
- ✅ 批量操作（`WriteBatch`, `MultiGet`）
- ✅ 列族（Column Family）支持
- ✅ 快照（Snapshot）
- ✅ 迭代器（Iterator）
- ✅ 压缩（Compaction）
- ✅ 外部文件导入（IngestExternalFile）
- ✅ 备份与恢复（BackupEngine）
- ✅ 检查点（Checkpoint）
- ✅ 事务（TransactionDB, OptimisticTransactionDB）
- ✅ 时间戳支持（Timestamp）
- ✅ 二级实例（Secondary Instance）

### ❌ 缺失功能

#### 1. SingleDelete
- **C++ API**: `DB::SingleDelete()`
- **功能**: 用于删除保证只写入一次且从未更新的键
- **状态**: 未实现
- **优先级**: 中

#### 2. GetMergeOperands
- **C++ API**: `DB::GetMergeOperands()`
- **功能**: 获取所有 merge 操作数，用于自定义 merge 逻辑
- **状态**: 未实现
- **优先级**: 中

#### 3. Resume
- **C++ API**: `DB::Resume()`
- **功能**: 恢复数据库操作（在暂停后）
- **状态**: 未实现
- **优先级**: 低

#### 4. Close
- **C++ API**: `DB::Close()`
- **功能**: 显式关闭数据库（当前 Rust 版本通过 Drop trait 自动关闭）
- **状态**: 未实现（但通过 Drop 提供类似功能）
- **优先级**: 低

#### 5. NewIterators
- **C++ API**: `DB::NewIterators()`
- **功能**: 为多个列族创建迭代器
- **状态**: 未实现
- **优先级**: 中

## 表属性与元数据

### ❌ 缺失功能

#### 6. GetPropertiesOfAllTables
- **C++ API**: `DB::GetPropertiesOfAllTables()`
- **功能**: 获取所有表的属性信息
- **状态**: 未实现
- **优先级**: 中

#### 7. GetPropertiesOfTablesInRange
- **C++ API**: `DB::GetPropertiesOfTablesInRange()`
- **功能**: 获取指定范围内的表属性
- **状态**: 未实现
- **优先级**: 中

## 事件监听器

### ❌ 缺失功能

#### 8. EventListener
- **C++ API**: `EventListener` 类
- **功能**: 监听数据库事件（压缩、刷新、写入等）
- **主要事件类型**:
  - `OnFlushCompleted` - 刷新完成
  - `OnFlushBegin` - 刷新开始
  - `OnCompactionCompleted` - 压缩完成
  - `OnCompactionBegin` - 压缩开始
  - `OnTableFileCreated` - 表文件创建
  - `OnTableFileDeleted` - 表文件删除
  - `OnBackgroundError` - 后台错误
  - `OnStallConditionsChanged` - 停滞条件变化
  - `OnFileDeletionStarted` - 文件删除开始
  - `OnSubcompactionBegin` - 子压缩开始
  - `OnSubcompactionCompleted` - 子压缩完成
- **相关 API**: `DBOptions::listeners` (vector of EventListener)
- **状态**: 完全未实现
- **优先级**: 高（对监控和调试很重要）

## 统计历史

### ❌ 缺失功能

#### 9. StatsHistoryIterator
- **C++ API**: `StatsHistoryIterator`
- **功能**: 迭代历史统计信息
- **相关 API**:
  - `DB::GetStatsHistory()`
  - `DBOptions::stats_history_buffer_size`
- **状态**: 未实现
- **优先级**: 中

## 追踪与调试

### ❌ 缺失功能

#### 10. TraceWriter / TraceReader
- **C++ API**: `TraceWriter`, `TraceReader`
- **功能**: 记录和回放数据库操作轨迹
- **相关 API**:
  - `DB::StartTrace()`
  - `DB::EndTrace()`
  - `DB::Replay()`
- **状态**: 未实现
- **优先级**: 中

#### 11. PerfContext 扩展
- **当前状态**: 部分实现（`PerfContext` 已存在）
- **缺失**: 一些高级性能指标
- **优先级**: 低

## 线程状态

### ❌ 缺失功能

#### 12. GetThreadList
- **C++ API**: `DB::GetThreadList()`
- **功能**: 获取当前线程状态信息
- **状态**: 未实现
- **优先级**: 低

## 文件系统操作

### ❌ 缺失功能

#### 13. 文件校验和
- **C++ API**: 
  - `IngestExternalFileArg` 中的 `files_checksums`
  - `TableFileCreationInfo` 中的 `file_checksum`
- **功能**: 支持文件校验和验证
- **状态**: 部分支持（SST 文件写入时支持，但读取和验证可能不完整）
- **优先级**: 中

## 高级选项

### ✅ 已实现
- ✅ 大部分 `DBOptions` 和 `ColumnFamilyOptions`
- ✅ 压缩选项
- ✅ 缓存选项
- ✅ 写入缓冲区管理

### ❌ 缺失功能

#### 14. 部分高级选项
- **C++ API**: 某些新的选项设置
- **功能**: 
  - 一些新版本添加的选项可能未完全暴露
  - 需要定期检查 C++ 版本更新
- **状态**: 需要定期审查
- **优先级**: 低

## 辅助功能

### ❌ 缺失功能

#### 15. PrepareForBulkLoad
- **C++ API**: `Options::PrepareForBulkLoad()`
- **功能**: 为批量加载优化配置
- **状态**: 未实现（但可以通过手动设置选项达到类似效果）
- **优先级**: 低

#### 16. OptimizeForPointLookup / OptimizeForSmallDb 等便捷方法
- **C++ API**: 各种 `OptimizeFor*` 方法
- **功能**: 便捷的配置预设
- **状态**: 部分实现（`optimize_for_point_lookup` 存在）
- **优先级**: 低

## 错误处理

### ❌ 缺失功能

#### 17. 错误恢复回调
- **C++ API**: `ErrorRecoveryContext` 和相关的错误恢复机制
- **功能**: 自定义错误恢复逻辑
- **状态**: 未实现
- **优先级**: 中

## 文件系统管理

### ✅ 已实现
- ✅ RateLimiter（速率限制器）

### ❌ 缺失功能

#### 18. SstFileManager
- **C++ API**: `SstFileManager`
- **功能**: 管理 SST 文件的删除和空间限制
- **相关 API**: `DBOptions::sst_file_manager`
- **状态**: 未实现
- **优先级**: 中（对生产环境重要）

#### 19. FileSystem
- **C++ API**: `FileSystem` 抽象类
- **功能**: 自定义文件系统接口（如支持远程文件系统）
- **相关 API**: `DBOptions::env` 和 `FileSystem` 相关选项
- **状态**: 部分支持（通过 Env 接口）
- **优先级**: 低（除非需要自定义文件系统）

## 总结

### 高优先级缺失功能
1. **EventListener** - 对监控和调试非常重要

### 中优先级缺失功能
2. **SingleDelete** - 特定场景下有用
3. **GetMergeOperands** - 自定义 merge 逻辑需要
4. **NewIterators** - 多列族迭代器
5. **GetPropertiesOfAllTables** - 元数据管理
6. **GetPropertiesOfTablesInRange** - 元数据管理
7. **StatsHistoryIterator** - 统计历史追踪
8. **TraceWriter/Reader** - 调试和回放
9. **文件校验和完整支持** - 数据完整性
10. **SstFileManager** - 文件管理（生产环境重要）

### 低优先级缺失功能
11. **Resume** - 不常用
12. **Close** - 已有 Drop trait
13. **GetThreadList** - 调试用
14. **部分便捷方法** - 可以通过手动配置替代
15. **FileSystem 自定义** - 除非需要特殊文件系统

## 建议的贡献顺序

1. **EventListener** - 最实用，影响最大
2. **SingleDelete** - 相对简单，功能明确
3. **GetMergeOperands** - 对 merge 操作重要
4. **NewIterators** - 多列族场景有用
5. **表属性相关 API** - 元数据管理

## 注意事项

- 本分析基于 RocksDB C++ 版本的最新稳定版本
- 某些功能可能通过底层 FFI 已可用但未在 Rust API 中暴露
- 建议定期检查 C++ RocksDB 的更新，确保功能同步
- 某些功能可能在 Rust 生态中有更好的替代方案

## 如何贡献

1. 查看 `librocksdb-sys` 中的 FFI 绑定，确认底层 C++ API 是否已绑定
2. 在 `src/` 目录下创建或修改相应的 Rust 模块
3. 添加测试用例（参考 `tests/` 目录）
4. 更新文档
5. 提交 PR
