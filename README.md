# OriginAgent v3.6

目标：

20% 高频封装 + 80% 通用执行器，并增加常用数据分析报告。

## 已封装高频能力

- Excel / CSV / TXT / DAT 导入
- 自动列名识别
- 自动 X/Y 选择
- 单曲线 / 多曲线
- line / scatter / column
- Origin 模板入口
- science 风格入口
- 多格式导出
- 保存 OPJU
- 日志
- 控制 Origin 是否保持打开
- analysis 字段：
  - `statistics`: pandas `describe()`
  - `linear_fit`: numpy `polyfit`，输出 slope / intercept / r2
  - `peak_analysis`: scipy `find_peaks`，无 scipy 时使用局部极大值兜底
  - `fft`: numpy FFT，输出主频和频谱 CSV
  - `pca`: numpy SVD，输出 scores / loadings CSV
  - `custom_labtalk`: 执行自定义 LabTalk

## 全功能兜底能力

- `labtalk`: 执行任意 Origin LabTalk
- `origin_python`: 执行任意 Origin Python

v3.6 增强了通用执行器可靠性：支持命令行指定任务文件、错误报告、错误堆栈日志、LabTalk 空脚本跳过与 `type -b` warning、Origin Python 空代码跳过与结构化异常返回。

## 分析输出

- `outputs/report.md`
- `outputs/fft_result.csv`
- `outputs/pca_scores.csv`
- `outputs/pca_loadings.csv`

## 运行

```powershell
cd C:\OriginAI\agent
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

## analysis 示例

```json
{
  "analysis": {
    "type": "linear_fit",
    "params": {
      "x": "Time",
      "y": "Temperature"
    }
  }
}
```
