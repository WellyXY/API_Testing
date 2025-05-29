# Advanced Recommendation System Formula (English)

## The CRMS (Comprehensive Relationship Matching Score) Algorithm

$$CRMS(u_i, u_j) = \alpha \cdot L(u_j) \cdot e^{-\beta \cdot D(u_i, u_j)} + \gamma \cdot R(u_i, u_j) \cdot \lambda \cdot A(u_j) + \delta \cdot S(u_i, u_j) + \epsilon \cdot H(u_i, u_j)$$

Where:

**Key Parameters:**
- $u_i$ = Source user (active user)
- $u_j$ = Target user (potential match)
- $L(u_j)$ = Like rate of target user $u_j$ (percentage of received positive interactions)
- $D(u_i, u_j)$ = Geographic distance function between users, normalized with exponential decay
- $R(u_i, u_j)$ = Relationship status coefficient defined as:
  $$R(u_i, u_j) = 
  \begin{cases} 
  1 & \text{if unmatch} \\
  1 + \log(1 + \frac{I(u_i, u_j)}{10}) & \text{if matched with intimacy score } I(u_i, u_j) \in [1,100]
  \end{cases}$$
- $A(u_j)$ = Active like rate of target user (measure of user engagement)
- $S(u_i, u_j)$ = Feature similarity vector calculated as:
  $$S(u_i, u_j) = \omega_e \cdot E(u_i, u_j) + \omega_w \cdot W(u_i, u_j) + \omega_i \cdot I(u_i, u_j)$$
  Where $E$, $W$, and $I$ represent education, work, and interest similarity respectively
- $H(u_i, u_j)$ = Historical matching similarity based on previous successful matches

**Hyperparameters:**
- $\alpha$ = Weight for like rate importance (typically 0.25)
- $\beta$ = Distance sensitivity factor (typically 0.1 km⁻¹)
- $\gamma$ = Weight for relationship status (typically 0.20)
- $\lambda$ = Weight for active engagement (typically 0.15)
- $\delta$ = Weight for feature similarity (typically 0.25)
- $\epsilon$ = Weight for historical matching patterns (typically 0.15)
- $\omega_e, \omega_w, \omega_i$ = Weights for education, work, and interest similarities within the feature vector

**Score Normalization:**
Final scores are normalized using min-max normalization to produce values between 0 and 1:

$$CRMS_{norm}(u_i, u_j) = \frac{CRMS(u_i, u_j) - CRMS_{min}}{CRMS_{max} - CRMS_{min}}$$

Users are then ranked by their normalized CRMS score, with recommendations prioritized for users with scores above the dynamic threshold $\theta_t$, which adapts based on user interaction history.

---

# 高级推荐系统公式（中文）

## CRMS（综合关系匹配分数）算法

$$CRMS(u_i, u_j) = \alpha \cdot L(u_j) \cdot e^{-\beta \cdot D(u_i, u_j)} + \gamma \cdot R(u_i, u_j) \cdot \lambda \cdot A(u_j) + \delta \cdot S(u_i, u_j) + \epsilon \cdot H(u_i, u_j)$$

其中：

**关键参数：**
- $u_i$ = 源用户（活跃用户）
- $u_j$ = 目标用户（潜在匹配对象）
- $L(u_j)$ = 目标用户$u_j$的被喜欢率（收到正面互动的百分比）
- $D(u_i, u_j)$ = 用户间地理距离函数，通过指数衰减进行归一化
- $R(u_i, u_j)$ = 关系状态系数，定义为：
  $$R(u_i, u_j) = 
  \begin{cases} 
  1 & \text{若未匹配} \\
  1 + \log(1 + \frac{I(u_i, u_j)}{10}) & \text{若已匹配且亲密度得分为 } I(u_i, u_j) \in [1,100]
  \end{cases}$$
- $A(u_j)$ = 目标用户的主动喜欢率（用户参与度的度量）
- $S(u_i, u_j)$ = 特征相似性向量，计算为：
  $$S(u_i, u_j) = \omega_e \cdot E(u_i, u_j) + \omega_w \cdot W(u_i, u_j) + \omega_i \cdot I(u_i, u_j)$$
  其中$E$、$W$和$I$分别代表教育、工作和兴趣相似性
- $H(u_i, u_j)$ = 基于以往成功匹配的历史匹配相似度

**超参数：**
- $\alpha$ = 喜欢率重要性权重（通常为0.25）
- $\beta$ = 距离敏感因子（通常为0.1 km⁻¹）
- $\gamma$ = 关系状态权重（通常为0.20）
- $\lambda$ = 活跃度权重（通常为0.15）
- $\delta$ = 特征相似性权重（通常为0.25）
- $\epsilon$ = 历史匹配模式权重（通常为0.15）
- $\omega_e, \omega_w, \omega_i$ = 特征向量中教育、工作和兴趣相似性的权重

**分数归一化：**
最终分数通过最小-最大归一化处理，生成0到1之间的值：

$$CRMS_{norm}(u_i, u_j) = \frac{CRMS(u_i, u_j) - CRMS_{min}}{CRMS_{max} - CRMS_{min}}$$

用户随后按照其归一化CRMS分数排名，优先推荐分数高于动态阈值$\theta_t$的用户，该阈值根据用户互动历史进行调整。 