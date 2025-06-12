# Request Body
```JSON
{
  "model_name_or_path": "facebook/opt-1.3b",
  "data_config": {
    "collection": "train step 1",
    "process_script": "preprocess_dataset.py",
    "dataset_class": "MyCustomDataset"
  },
  "training_config": {
    "method": "rft",
    "training_arguments": {
      "lr": 5e-6,
      "optim": "adamw",
      "gpus": 4,
      "steps": 50000
    },
    "algorithm": "ppo",  // or "grpo" if customized gradient-based policy
    "scoring_script": "reward_fn.py",
    "scoring_class": "CustomRewardScorer"
  },
  "output_config": {
    "save_chks_path": "./checkpoints",
    "sync_with_samplers": true
  }
}
```

# Structure

```bash
training_service/
├── main.py                    # FastAPI 启动入口
├── api/
│   └── endpoints.py           # 路由定义（接收训练请求）
├── schemas/
│   ├── training_request.py    # 请求体结构
│   ├── task_info.py           # task 状态、进度定义
│   └── gpu_info.py            # GPU 资源结构定义
├── services/
│   ├── training_dispatcher.py # 核心调度服务（调用下面这些）
│   ├── training_launcher      # 启动训练服务
│   ├── resource_service.py    # GPU & 节点资源
│   ├── scheduler_service.py   # 资源调度
│   ├── task_service.py        # task 状态注册、查询
│   ├── monitor_service.py     # 训练任务运行状态监控
│   └── sync_service.py        # 权重同步 / 回传给 sampler
├── infra/
│   ├── gpu_monitor.py         # GPU 状态检查（nvidia-smi 等）
│   ├── shell_runner.py        # SSH远程训练任务执行
│   └── file_watcher.py        # 日志/状态文件监听
└── utils/
    └── logger.py              # 日志封装



```

# Example



