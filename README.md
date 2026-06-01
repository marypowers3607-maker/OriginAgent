# OriginAgent v4.0

目标：

20% 高频封装 + 80% 通用执行器，并增加规则式自然语言任务规划器。

## 自然语言规划

`planner.py` 不调用大模型，只用关键词和规则把自然语言转换成 JSON 任务文件：

```powershell
cd C:\OriginAI\agent
py planner.py "读取 C:/OriginAI/data/test.xlsx，画 Temperature 随 Time 变化的折线图，做 FFT，导出 PNG 和 TIFF，保存 OPJU，生成报告"
```

输出：

```text
C:\OriginAI\agent\requests\planned_task.json
```

也可以规划并立即执行：

```powershell
py run_planned.py "读取 C:/OriginAI/data/test.xlsx，画 Temperature 随 Time 变化的折线图，做 FFT，导出 PNG 和 TIFF"
```

等价于：

```powershell
py planner.py "..."
py task_runner.py requests/planned_task.json
```

## 规则关键词

- 折线图 / `line` -> `plot_type: line`
- 散点图 / `scatter` -> `plot_type: scatter`
- 柱状图 / `column` / `bar` -> `plot_type: column`
- `statistics` / 描述性统计 -> `analysis: statistics`
- `linear fit` / 线性拟合 -> `analysis: linear_fit`
- `fft` / 频谱 -> `analysis: fft`
- `pca` / 主成分 -> `analysis: pca`
- `peak` / 峰值 -> `analysis: peak_analysis`
- `png` / `tif` / `tiff` / `pdf` -> export paths
- 保存 OPJU -> `save_project: true`
- 生成报告 -> `report: true`

自动识别 `C:/...` 和 `C:\...` 作为 `input_file`。

支持 X/Y 表达：

```text
Temperature 随 Time 变化
以 Time 为 X，Temperature 为 Y
```

## JSON 运行

```powershell
py task_runner.py
py task_runner.py requests/fft_test.json
py task_runner.py requests/pca_test.json
py task_runner.py requests/peak_test.json
py task_runner.py C:/OriginAI/agent/requests/pca_test.json
```

未传任务文件参数时，默认使用：

```text
C:\OriginAI\agent\requests\demo_task.json
```

## 已封装能力

- Excel / CSV / TXT / DAT 导入
- 自动列名识别
- 自动 X/Y 选择
- line / scatter / column
- Origin 模板入口
- science 风格入口
- 多格式导出
- 保存 OPJU
- 日志与错误报告
- LabTalk 与 Origin Python 兜底执行

## 分析输出

- `outputs/report.md`
- `outputs/fft_result.csv`
- `outputs/pca_scores.csv`
- `outputs/pca_loadings.csv`
