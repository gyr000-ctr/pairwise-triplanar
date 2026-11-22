"""triplanar 核心 API。

三平面纹理映射权重：按法线各分量绝对值的 sharpness 次幂归一化，
权重和恒为 1，轴对齐法线退化为单平面。实现无可变共享状态，并发安全。
"""

import math

__all__ = ["Triplanar"]


class Triplanar:
    __slots__ = ("_sharpness",)

    def __init__(self, sharpness=1.0):
        """构造。sharpness 必须为正的有限实数，否则抛 ValueError。"""
        if isinstance(sharpness, bool) or not isinstance(sharpness, (int, float)):
            raise ValueError("sharpness 必须为实数")
        sharpness = float(sharpness)
        if not math.isfinite(sharpness) or sharpness <= 0.0:
            raise ValueError("sharpness 必须为正的有限值")
        self._sharpness = sharpness

    def weights(self, normal):
        """三平面权重，返回长度为 3 的 float 元组，和为 1。"""
        try:
            nx, ny, nz = normal
        except TypeError:
            raise ValueError("normal 必须为三分量序列") from None
        except ValueError:
            raise ValueError("normal 必须恰好有三个分量") from None

        ax = abs(nx)
        ay = abs(ny)
        az = abs(nz)

        if not (math.isfinite(ax) and math.isfinite(ay) and math.isfinite(az)):
            raise ValueError("normal 分量必须为有限数值")

        total = ax + ay + az
        if total == 0.0:
            raise ValueError("零法线无定义")

        k = self._sharpness
        if k == 1.0:
            inv = 1.0 / total
            return (ax * inv, ay * inv, az * inv)

        wx = ax ** k
        wy = ay ** k
        wz = az ** k
        s = wx + wy + wz
        if s == 0.0:
            # 极端 sharpness 下三个分量均下溢为 0：退化为最大分量独占
            if ax >= ay and ax >= az:
                return (1.0, 0.0, 0.0)
            if ay >= az:
                return (0.0, 1.0, 0.0)
            return (0.0, 0.0, 1.0)
        inv = 1.0 / s
        return (wx * inv, wy * inv, wz * inv)
