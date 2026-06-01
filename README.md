# OriginAgent v4.1

目标：

20% 高频封装 + 80% 通用执行器。v4.1 在不推翻现有架构的前提下，增加样式桥、模板桥和批处理脚手架。

## 推荐用法

优先使用常用 JSON 字段和自然语言规划器：

```powershell
py run_planned.py "读取 C:/OriginAI/data/test.xlsx，画 Temperature 随 Time 变化的折线图，做 FFT，导出 PNG 和 TIFF，保存 OPJU，生成报告"
```

遇到复杂 Origin 图形控制时，不建议继续堆高层字段，使用通用执行器兜底：

- `style_commands`: 样式桥，支持 `origin_python` 或 `labtalk`
- `origin_python`: 直接执行 OriginPro Python
- `labtalk`: 直接执行 LabTalk

## 自然语言规划

`planner.py` 不调用大模型，只用关键词和规则把自然语言转换成 JSON 任务文件：

```powershell
py planner.py "读取 C:/OriginAI/data/test.xlsx，画 Temperature 随 Time 变化的折线图，做 FFT，红色，线宽2，虚线，Arial，导出 PNG 和 TIFF"
```

输出：

```text
C:\OriginAI\agent\requests\planned_task.json
```

支持：

- 折线图 / `line`
- 散点图 / `scatter`
- 柱状图 / `column` / `bar`
- `statistics` / 描述性统计
- `linear fit` / 线性拟合
- `fft` / 频谱
- `pca` / 主成分
- `peak` / 峰值
- `png` / `tif` / `tiff` / `pdf`
- 保存 OPJU
- 生成报告
- 所有数值列 / 多曲线 / 全部Y列
- 红色 / 蓝色 / 绿色 / 黑色
- 线宽2 / 线宽3
- 虚线 / 实线 / 点线
- Arial / Times New Roman

## 样式桥

`style_commands` 是稳定入口，不把所有 Origin 样式硬封装进绘图函数。

```json
{
  "style_commands": [
    {
      "type": "origin_python",
      "code": "outputs.setdefault('style_requests', []).append({'color': 'red', 'line_width': 2})"
    },
    {
      "type": "labtalk",
      "script": "layer -a;"
    }
  ]
}
```

planner 识别到颜色、线宽、线型、字体时，会先转换为 `style_commands`。项目需要更细粒度 Origin 控制时，可以在这个入口里写 OriginPro Python 或 LabTalk。

## 模板桥

`template` 字段保留轻量接口：

- `null`: 不使用模板
- `"line"`: 使用内置 line plot 逻辑
- `"scatter"`: 使用内置 scatter plot 逻辑
- `"column"` / `"bar"`: 使用内置 column plot 逻辑
- `"custom_path_or_name"`: 传给 Origin graph template 接口

先不强依赖具体 `.otpu` 文件，后续可以把常用模板名映射到团队模板路径。

## 批处理

`tools/batch.py` 提供基础扫描入口，JSON 任务可以使用同一任务模板处理文件夹中的多个文件：

```json
{
  "batch": {
    "folder": "C:/OriginAI/data",
    "pattern": "*.xlsx"
  },
  "plot": true,
  "plot_type": "line",
  "x": "Time",
  "auto_all_y": true
}
```

这会扫描匹配文件，并对每个文件复用同一任务模板。

## JSON 运行

```powershell
py task_runner.py
py task_runner.py requests/style_test.json
py task_runner.py requests/batch_test.json
py task_runner.py requests/fft_test.json
py task_runner.py C:/OriginAI/agent/requests/pca_test.json
```

未传任务文件参数时，默认使用：

```text
C:\OriginAI\agent\requests\demo_task.json
```

## 已保留能力

- `planner.py`
- `run_planned.py`
- `task_runner.py`
- JSON task 结构
- `tools/execute_labtalk.py`
- `tools/execute_origin_python.py`
- analysis: `statistics`, `linear_fit`, `fft`, `peak_analysis`, `pca`
- report 输出

## 分析输出

- `outputs/report.md`
- `outputs/fft_result.csv`
- `outputs/pca_scores.csv`
- `outputs/pca_loadings.csv`
