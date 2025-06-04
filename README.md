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
├── main.py                    # FastAPI 入口
├── api/
│   └── endpoints.py           # API 路由定义
├── schemas/
│   └── training_request.py    # 请求体结构定义（Pydantic）
├── services/
│   ├── trainer_factory.py     # 根据请求动态选择训练方法（如 PPO/GPRO）
│   ├── config_builder.py      # 将请求体转换为训练统一配置
│   └── task_manager.py        # 启动/管理异步训练任务
├── trainers/
│   ├── base.py                # 所有 Trainer 的抽象基类
│   ├── ppo_trainer.py         # PPO 实现
│   └── gpro_trainer.py        # GPRO 实现
├── utils/
│   └── logger.py              # 日志封装
│   └── runner.py              # subprocess 脚本执行器
└── models/
    └── model_manager.py       # 训练后模型的保存/回传逻辑

```

# Example

