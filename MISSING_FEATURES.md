# Rust RocksDB 缺失功能对比报告

## 概述
本文档对比了 Rust RocksDB 实现与 C++ 版本 RocksDB 的功能，列出了当前缺失的主要功能。

## 一、核心操作 API

### 1. SingleDelete 操作
**状态**: ❌ 缺失
- **C++ API**: `DB::SingleDelete()`, `WriteBatch::SingleDelete()`
- **描述**: 用于删除只写入过一次的键，性能优化功能
- **影响**: 缺少性能优化选项

### 2. GetMergeOperands
**状态**: ❌ 缺失
- **C++ API**: `DB::GetMergeOperands()`
- **描述**: 获取合并操作的所有操作数，用于自定义合并逻辑
- **影响**: 限制了自定义合并操作的实现

## 二、数据库管理功能

### 3. Close 方法
**状态**: ❌ 缺失（隐式处理）
- **C++ API**: `DB::Close()`
- **描述**: 显式关闭数据库，释放资源
- **影响**: Rust 版本通过 Drop trait 处理，但缺少显式关闭和错误处理

### 4. Resume 方法
**状态**: ❌ 缺失
- **C++ API**: `DB::Resume()`
- **描述**: 恢复数据库操作
- **影响**: 某些场景下可能需要显式恢复

### 5. CompactFiles
**状态**: ❌ 缺失
- **C++ API**: `DB::CompactFiles()`
- **描述**: 压缩指定的文件列表到指定级别
- **影响**: 无法精细控制文件压缩

### 6. EnableAutoCompaction
**状态**: ❌ 缺失
- **C++ API**: `DB::EnableAutoCompaction()`
- **描述**: 启用自动压缩（如果之前被禁用）
- **影响**: 无法动态控制自动压缩

### 7. DisableManualCompaction / EnableManualCompaction
**状态**: ❌ 缺失
- **C++ API**: `DB::DisableManualCompaction()`, `DB::EnableManualCompaction()`
- **描述**: 禁用/启用手动压缩
- **影响**: 无法控制手动压缩的启用状态

### 8. PauseBackgroundWork / ContinueBackgroundWork
**状态**: ❌ 缺失
- **C++ API**: `DB::PauseBackgroundWork()`, `DB::ContinueBackgroundWork()`
- **描述**: 暂停/恢复后台工作（压缩、刷新等）
- **影响**: 无法控制后台任务的执行

### 9. NumberLevels
**状态**: ❌ 缺失
- **C++ API**: `DB::NumberLevels()`
- **描述**: 获取列族的级别数
- **影响**: 无法查询数据库结构信息

### 10. MaxMemCompactionLevel
**状态**: ❌ 缺失
- **C++ API**: `DB::MaxMemCompactionLevel()`
- **描述**: 获取最大内存压缩级别
- **影响**: 无法查询压缩配置信息

### 11. Level0StopWriteTrigger
**状态**: ❌ 缺失
- **C++ API**: `DB::Level0StopWriteTrigger()`
- **描述**: 获取触发 L0 停止写入的阈值
- **影响**: 无法查询写入控制信息

## 三、WAL 和文件管理

### 12. SyncWAL
**状态**: ❌ 缺失
- **C++ API**: `DB::SyncWAL()`
- **描述**: 同步 WAL 到磁盘
- **影响**: 无法显式同步 WAL（当前只有 FlushWAL）

### 13. LockWAL / UnlockWAL
**状态**: ❌ 缺失
- **C++ API**: `DB::LockWAL()`, `DB::UnlockWAL()`
- **描述**: 锁定/解锁 WAL，防止刷新
- **影响**: 无法控制 WAL 刷新行为

### 14. GetCurrentWalFile
**状态**: ❌ 缺失
- **C++ API**: `DB::GetCurrentWalFile()`
- **描述**: 获取当前 WAL 文件路径
- **影响**: 无法查询当前 WAL 状态

### 15. GetLiveFiles (带参数)
**状态**: ⚠️ 部分实现
- **C++ API**: `DB::GetLiveFiles(std::vector<std::string>&, uint64_t*)`
- **描述**: 获取活动文件列表和清单文件编号
- **影响**: Rust 版本有 `live_files()` 但可能缺少某些参数

### 16. GetLiveFilesMetaData
**状态**: ❌ 缺失
- **C++ API**: `DB::GetLiveFilesMetaData()`
- **描述**: 获取活动文件的元数据
- **影响**: 无法获取详细的文件元数据

### 17. NewIterators (批量)
**状态**: ❌ 缺失
- **C++ API**: `DB::NewIterators()`
- **描述**: 批量创建多个迭代器
- **影响**: 无法高效批量创建迭代器

## 四、统计和监控功能

### 18. ResetStats
**状态**: ❌ 缺失
- **C++ API**: `DB::ResetStats()`
- **描述**: 重置统计信息
- **影响**: 无法重置统计计数器

### 17. GetStatsHistory
**状态**: ❌ 缺失
- **C++ API**: `DB::GetStatsHistory()`
- **描述**: 获取统计历史记录
- **影响**: 无法访问历史统计数据

### 18. StatsHistoryIterator
**状态**: ❌ 缺失
- **C++ API**: `StatsHistoryIterator`
- **描述**: 迭代统计历史记录
- **影响**: 无法遍历历史统计

## 五、追踪和调试功能

### 21. StartTrace / EndTrace
**状态**: ❌ 缺失
- **C++ API**: `DB::StartTrace()`, `DB::EndTrace()`
- **描述**: 开始/结束追踪操作
- **影响**: 无法追踪数据库操作

### 22. StartIOTrace / EndIOTrace
**状态**: ❌ 缺失
- **C++ API**: `DB::StartIOTrace()`, `DB::EndIOTrace()`
- **描述**: 开始/结束 IO 追踪
- **影响**: 无法追踪 IO 操作

### 23. StartBlockCacheTrace / EndBlockCacheTrace
**状态**: ❌ 缺失
- **C++ API**: `DB::StartBlockCacheTrace()`, `DB::EndBlockCacheTrace()`
- **描述**: 开始/结束块缓存追踪
- **影响**: 无法追踪缓存行为

### 24. TraceWriter
**状态**: ❌ 缺失
- **C++ API**: `TraceWriter`
- **描述**: 追踪写入器接口
- **影响**: 无法自定义追踪输出

## 六、事件监听

### 25. EventListener
**状态**: ❌ 缺失
- **C++ API**: `EventListener`
- **描述**: 监听数据库事件（压缩、刷新等）
- **影响**: 无法监听数据库事件

## 七、高级功能

### 26. PutEntity / DeleteEntity
**状态**: ❌ 缺失
- **C++ API**: `DB::PutEntity()`, `DB::DeleteEntity()`, `WriteBatch::PutEntity()`
- **描述**: 实体 API，支持宽列存储
- **影响**: 不支持宽列存储功能

### 27. CreateColumnFamilyWithImport
**状态**: ❌ 缺失
- **C++ API**: `DB::CreateColumnFamilyWithImport()`
- **描述**: 创建列族并导入数据
- **影响**: 无法在创建列族时导入数据

### 28. ImportColumnFamily
**状态**: ❌ 缺失
- **C++ API**: `DB::ImportColumnFamily()`
- **描述**: 导入列族
- **影响**: 缺少导入列族功能

### 29. IngestExternalFiles (批量版本)
**状态**: ⚠️ 部分实现
- **C++ API**: `DB::IngestExternalFiles()` (接受多个 IngestExternalFileArg)
- **描述**: 批量导入外部文件
- **影响**: Rust 版本可能只支持单列族导入

### 30. GetPropertiesOfAllTables
**状态**: ❌ 缺失
- **C++ API**: `DB::GetPropertiesOfAllTables()`
- **描述**: 获取所有表的属性
- **影响**: 无法批量获取表属性

### 31. GetPropertiesOfTablesInRange
**状态**: ❌ 缺失
- **C++ API**: `DB::GetPropertiesOfTablesInRange()`
- **描述**: 获取指定范围内的表属性
- **影响**: 无法按范围获取表属性

### 32. SuggestCompactRange
**状态**: ❌ 缺失
- **C++ API**: `DB::SuggestCompactRange()`
- **描述**: 建议压缩范围
- **影响**: 无法获取压缩建议

### 33. PromoteL0
**状态**: ❌ 缺失
- **C++ API**: `DB::PromoteL0()`
- **描述**: 提升 L0 文件到更高级别
- **影响**: 无法手动提升文件级别

## 八、验证功能

### 34. VerifyFileChecksums
**状态**: ❌ 缺失
- **C++ API**: `DB::VerifyFileChecksums()`
- **描述**: 验证文件校验和
- **影响**: 无法验证数据完整性

### 35. VerifyChecksum
**状态**: ❌ 缺失
- **C++ API**: `DB::VerifyChecksum()`
- **描述**: 验证校验和
- **影响**: 无法验证数据完整性

## 九、WriteBatch 扩展

### 36. WriteBatch::SingleDelete
**状态**: ❌ 缺失
- **C++ API**: `WriteBatch::SingleDelete()`
- **描述**: WriteBatch 中的 SingleDelete 操作
- **影响**: 批量操作中缺少 SingleDelete

### 37. WriteBatch::PutEntity
**状态**: ❌ 缺失
- **C++ API**: `WriteBatch::PutEntity()`
- **描述**: WriteBatch 中的实体写入
- **影响**: 批量操作中缺少实体 API

### 38. WriteBatch::DeleteEntity
**状态**: ❌ 缺失
- **C++ API**: `WriteBatch::DeleteEntity()`
- **描述**: WriteBatch 中的实体删除
- **影响**: 批量操作中缺少实体 API

## 十、文件系统 API

### 39. GetFileSystem
**状态**: ❌ 缺失
- **C++ API**: `DB::GetFileSystem()`
- **描述**: 获取文件系统接口
- **影响**: 无法访问底层文件系统

## 十二、二级数据库功能

### 39. TryCatchUpWithPrimary (已部分实现)
**状态**: ✅ 已实现
- **C++ API**: `DB::TryCatchUpWithPrimary()`
- **描述**: 二级实例追赶主实例
- **状态**: Rust 版本有 `try_catch_up_with_primary()`

## 总结

### 优先级分类

#### 高优先级（核心功能）
1. SingleDelete - 性能优化功能
2. GetMergeOperands - 自定义合并必需
3. Close - 资源管理
4. SyncWAL - WAL 同步控制
5. PauseBackgroundWork / ContinueBackgroundWork - 后台任务控制

#### 中优先级（管理功能）
6. CompactFiles - 精细压缩控制
7. EnableAutoCompaction - 动态控制
8. LockWAL / UnlockWAL - WAL 控制
9. ResetStats - 统计管理
10. NewIterators - 批量迭代器创建

#### 低优先级（高级功能）
11. EventListener - 事件监听
12. 追踪功能 (StartTrace, StartIOTrace, etc.)
13. PutEntity / DeleteEntity - 宽列存储
14. StatsHistory - 历史统计

### 建议实施顺序

1. **第一阶段**: SingleDelete, GetMergeOperands, Close, SyncWAL, PauseBackgroundWork
2. **第二阶段**: CompactFiles, EnableAutoCompaction, LockWAL, ResetStats, NewIterators
3. **第三阶段**: EventListener, 追踪功能, 实体 API
4. **第四阶段**: 其他高级功能（验证、导入、统计历史等）

### 注意事项

- 某些功能可能由于 Rust 所有权模型需要不同的设计
- 某些功能需要额外的 FFI 绑定
- 建议先查看 C++ 头文件确认 API 签名
- 需要确保与现有 Rust API 设计风格一致
