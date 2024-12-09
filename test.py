import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 读取 Excel 文件
file_path = 'data.xlsx'  # 请确保 data.xlsx 文件在当前工作目录中，或提供完整路径
df = pd.read_excel(file_path)

# 确认数据
print("数据预览：")
print(df.head())

# 确保列名正确（根据实际情况调整）
expected_columns = ['ph', 'v', '∆ph', '∆v', '∆ph/∆v', '`V', '∆(∆PH/∆V)', '∆`V', '∆(∆ph/∆v)/∆v']
if not all(column in df.columns for column in expected_columns):
    raise ValueError(f"Excel 文件缺少预期的列。预期列：{expected_columns}")

# 确保数据按 'v' 排序（如果需要）
df = df.sort_values(by='v').reset_index(drop=True)

# 图表1：ph 对 v 的连续曲线图，标出斜率最大处的 v
plt.figure(figsize=(10, 6))
plt.plot(df['v'], df['ph'], marker='o', label='ph vs v')

# 计算斜率
slope = np.gradient(df['ph'], df['v'])
df['slope'] = slope

# 找到斜率最大的点
max_slope_idx = df['slope'].idxmax()
max_slope_v = df.loc[max_slope_idx, 'v']
max_slope_ph = df.loc[max_slope_idx, 'ph']

# 标记该点
plt.plot(max_slope_v, max_slope_ph, 'ro', label='最大斜率点')
plt.axvline(x=max_slope_v, linestyle='--', color='r')

# 设置坐标轴格式
plt.xlabel('v', fontsize=12)
plt.ylabel('ph', fontsize=12)
plt.title('ph vs v', fontsize=14)
plt.legend()
plt.grid(True)

# 设置刻度保留两位小数
plt.xticks(np.round(df['v'], 2))
plt.yticks(np.round(df['ph'], 2))

# 优化布局
plt.tight_layout()
plt.show()

# 图表2：∆ph/∆v 对 `V` 的连续曲线图，标出 ∆ph/∆v 的极大值
plt.figure(figsize=(10, 6))
plt.plot(df['`V'], df['∆ph/∆v'], marker='o', label='∆ph/∆v vs `V`')

# 找到 ∆ph/∆v 的最大值
max_dph_dv = df['∆ph/∆v'].max()
max_dph_dv_idx = df['∆ph/∆v'].idxmax()
max_dph_dv_V = df.loc[max_dph_dv_idx, '`V`']

# 标记该点
plt.plot(max_dph_dv_V, max_dph_dv, 'ro', label='极大值点')
plt.axvline(x=max_dph_dv_V, linestyle='--', color='r')

# 设置坐标轴格式
plt.xlabel('`V`', fontsize=12)
plt.ylabel('∆ph/∆v', fontsize=12)
plt.title('∆ph/∆v vs `V`', fontsize=14)
plt.legend()
plt.grid(True)

# 设置刻度保留两位小数
plt.xticks(np.round(df['`V`'], 2))
plt.yticks(np.round(df['∆ph/∆v'], 2))

# 优化布局
plt.tight_layout()
plt.show()

# 图表3：∆(∆ph/∆v)/∆v 对 ∆`V` 的连续曲线图，标出极大正值、极大负值及与零线相交的点
plt.figure(figsize=(10, 6))
plt.plot(df['∆`V`'], df['∆(∆ph/∆v)/∆v'], marker='o', label='∆(∆ph/∆v)/∆v vs ∆`V`')

# 找到极大正值和极大负值
max_positive = df['∆(∆ph/∆v)/∆v'].max()
max_positive_idx = df['∆(∆ph/∆v)/∆v'].idxmax()
max_positive_V = df.loc[max_positive_idx, '∆`V`']

max_negative = df['∆(∆ph/∆v)/∆v'].min()
max_negative_idx = df['∆(∆ph/∆v)/∆v'].idxmin()
max_negative_V = df.loc[max_negative_idx, '∆`V`']

# 标记极大正值点
plt.plot(max_positive_V, max_positive, 'ro', label='极大正值点')
plt.axvline(x=max_positive_V, linestyle='--', color='r')

# 标记极大负值点
plt.plot(max_negative_V, max_negative, 'bo', label='极大负值点')
plt.axvline(x=max_negative_V, linestyle='--', color='b')

# 找到与零线相交的点
# 通过线性插值找到 ∆`V` 对应的零点
zero_crossings = np.where(np.diff(np.sign(df['∆(∆ph/∆v)/∆v'])))[0]
zero_V = []
for idx in zero_crossings:
    V1 = df.loc[idx, '∆`V`']
    V2 = df.loc[idx + 1, '∆`V`']
    y1 = df.loc[idx, '∆(∆ph/∆v)/∆v']
    y2 = df.loc[idx + 1, '∆(∆ph/∆v)/∆v']
    # 线性插值计算零点
    if y2 - y1 != 0:
        V_zero = V1 - y1 * (V2 - V1) / (y2 - y1)
        zero_V.append(V_zero)
        plt.plot(V_zero, 0, 'go', label='与零线相交点' if len(zero_V) == 1 else "")
        plt.axvline(x=V_zero, linestyle='--', color='g')

# 设置坐标轴格式
plt.xlabel('∆`V`', fontsize=12)
plt.ylabel('∆(∆ph/∆v)/∆v', fontsize=12)
plt.title('∆(∆ph/∆v)/∆v vs ∆`V`', fontsize=14)
plt.legend()
plt.grid(True)

# 设置刻度保留两位小数
plt.xticks(np.round(df['∆`V`'], 2))
plt.yticks(np.round(df['∆(∆ph/∆v)/∆v'], 2))

# 优化布局
plt.tight_layout()
plt.show()
