\documentclass[12pt, a4paper]{article}

% ====== Packages / 宏包 ======
\usepackage[utf8]{inputenc}
\usepackage{geometry}
\geometry{a4paper, margin=1in} % 标准 1 英寸页边距
\usepackage{graphicx} % 插入图片宏包
\usepackage{caption}  % 图片标题宏包
\usepackage{hyperref} % 超链接宏包
\usepackage{chngcntr} % 用于修改计数器格式
\usepackage{setspace} % 行距控制
\usepackage{float}    % 强制图片位置选项 [H]

% 设置超链接样式
\hypersetup{
    colorlinks=true,
    linkcolor=blue,
    filecolor=magenta,      
    urlcolor=blue,
    citecolor=black,
}

% 设置图表编号随 section 变化 (例如 Figure 6.1, 6.2)
\counterwithin{figure}{section}

% 设置 1.5 倍行距 (学术论文常用)
\onehalfspacing

\begin{document}

% ==========================================
% Chapter 5: Rationale
% ==========================================
\section{Rationale for the Group's Approach to Exploring the Data}
\label{sec:rationale}

Given the multi-source panel data containing extensive spatial and temporal information, our exploratory data analysis (EDA) extends beyond basic descriptive statistics. We developed a progressive exploration strategy focusing on spatial distribution, temporal evolution, social dynamics, and economic logic. This approach aims not merely to visualize the data, but to test underlying assumptions and examine complex relationships among variables, thereby establishing a rigorous methodological foundation for subsequent advanced modeling (e.g., two-way fixed effects and machine learning). The specific strategies and their rationales are detailed below:

\subsection{Visual Exploration of Spatial Heterogeneity}
The adoption of electric vehicles (EVs) and the deployment of charging infrastructure often exhibit significant spatial clustering. Relying solely on macroscopic averages at the national or country level can obscure true variations at the local level. Therefore, this study integrated GeoJSON boundary data to construct multi-scale spatial heatmaps. This strategy aims to visually identify leading regions with high penetration rates as well as lagging areas, thereby clarifying the specific distribution of spatial heterogeneity. This not only illustrates the geographical evolution over different years but also provides statistical justification for introducing "Regional Fixed Effects" in the subsequent panel regression model to control for unobservable spatial characteristics.

\subsection{Temporal Trend Analysis of Regional Disparities}
After confirming spatial differences, it is necessary to further analyze how this imbalance changes over time. By extracting and comparing historical data spanning over a decade from regions with high and low penetration rates, we plotted time-series line charts. The primary purpose of this analysis is to examine whether regional gaps are converging or widening over time. Observing the changes in temporal trajectories across different regions helps assess long-term development trends and demonstrates that simple linear time extrapolation may not accurately reflect complex future growth patterns. This provides contextual justification for selecting prediction models capable of handling non-linear trends in later stages.

\subsection{Cross-sectional Analysis of Car Ownership and EV Penetration}
Conventional wisdom often assumes that regions with higher overall car ownership will correspondingly exhibit higher EV penetration rates. To test this assumption, this study conducted a cross-sectional comparative analysis of car ownership and EV penetration rates across regions, aiming to distinguish between "general vehicle demand" and "preference for new energy vehicles." The analysis reveals that some regions with lower overall car ownership actually exhibit higher EV penetration rates. This suggests that, at the current stage, EV consumption may be constrained by higher purchasing thresholds or specific economic conditions. Therefore, in subsequent variable selection and modeling, merely controlling for the total volume of vehicles is insufficient; the research focus should shift toward more fundamental explanatory variables such as income levels and infrastructure.

\subsection{Baseline Correlation Testing of Economic Variables}
Building on the previous discussion regarding consumption thresholds, this section presents a bivariate scatter analysis of Gross Disposable Household Income (GDHI) per head and EV penetration. A preliminary fitting was conducted without introducing other control variables to visually present the baseline correlation between economic levels and EV adoption. This step establishes the initial link between income levels and technology adoption, while also exposing the limitations of univariate observation: since high-income regions typically possess denser charging infrastructure, a potential confounding effect exists between the two. This baseline testing demonstrates that relying solely on descriptive statistics is inadequate to reveal the true drivers, thereby justifying the necessity of employing multiple regression and fixed effects models later to isolate confounding variables.

\subsection{Data Distribution Testing and Anomaly Identification}
Before constructing predictive models, examining the statistical distribution of core variables and identifying potential anomalous samples are critical steps to ensure model robustness. This study plotted the distribution histogram of EV penetration rates at the Local Authority District (LAD) level and conducted anomaly identification using scatter plots combined with economic indicators. Because real-world technology adoption processes often do not follow a strict normal distribution (frequently exhibiting right-skewed characteristics), this step helps clarify the foundational shape of the data. Furthermore, the purpose of anomaly testing lies not only in data quality control but also in identifying specific regions that deviate from general trends (e.g., regions with high income but low penetration, or low income but high penetration). This indicates that global linear models may be distorted by extreme samples, thus providing empirical support for the subsequent introduction of machine learning algorithms capable of accommodating non-linear relationships (such as XGBoost), as well as the use of fixed effects to control for local heterogeneity.

% ==========================================
% Chapter 6: EDA and Findings
% ==========================================
\section{Exploratory Data Analysis and Preliminary Findings}
\label{sec:eda}

Having established a multi-dimensional exploration strategy, this study conducted a systematic visual analysis of the reconstructed panel data. The following preliminary findings objectively illustrate the spatial and temporal statistical characteristics of EV adoption in the UK, providing empirical evidence for the subsequent construction of econometric models and machine learning frameworks.

\subsection{Visual Analysis of Spatial Distribution Characteristics}
To examine the spatial distribution characteristics of EV penetration, this study plotted a macroscopic regional heatmap of the UK based on the merged GeoJSON boundary data.

% --- Figure 6.1 Placeholder ---
\begin{figure}[H]
    \centering
    % 请将 'example-image' 替换为您的实际图片文件名，如 'heatmap.png'
    \includegraphics[width=0.85\textwidth]{example-image}
    \caption{Snapshot of the spatial heatmap of EV penetration across UK regions. \\ \textit{Note: This is a snapshot of the interactive heatmap webpage developed by our team. For a multi-scale dynamic display spanning 2011-2025, please visit the full interactive dashboard online at: \url{https://song-jp.github.io/UK_EV_Map/} (See Appendix A for detailed usage instructions).}}
    \label{fig:heatmap}
\end{figure}

As shown in Figure \ref{fig:heatmap}, EV adoption is not uniformly distributed across the UK but exhibits significant spatial clustering. Economically developed southern regions (such as Greater London and the South East) appear in dark red, indicating relatively high penetration rates. In contrast, the regional colors for Wales, Northern Ireland, and certain northern areas are noticeably lighter. This phenomenon confirms the existence of distinct regional disparities in adoption rates. This finding suggests that it is necessary to introduce Regional Fixed Effects in the subsequent regression modeling to absorb unobservable spatial heterogeneity errors.

\subsection{Time-Series Trend Characteristics of Regional Disparities}
Having identified spatial distribution disparities, this study further extracted representative regions with higher and lower penetration rates to plot a time-series trend chart spanning over a decade, aiming to observe the dynamic evolution of these differences.

% --- Figure 6.2 Placeholder ---
\begin{figure}[H]
    \centering
    \includegraphics[width=0.85\textwidth]{example-image}
    \caption{Comparative trend chart of regional EV penetration evolution (Leading vs. Lagging Regions)}
    \label{fig:trend_gap}
\end{figure}

As illustrated in Figure \ref{fig:trend_gap}, during the 2011-2018 period, penetration rates in all regions remained at a low level, and regional gaps were minimal. Since 2019, the growth curves of leading regions (such as London and the South East) have shown a significant upward trajectory, while the growth in some lagging regions (such as Wales and Northern Ireland) has remained relatively flat. By 2025, the absolute gap in penetration rates between the two ends has expanded to approximately 7\%. This dynamic trajectory indicates that regional disparities in adoption rates are widening over time, and simple linear time extrapolation cannot accurately fit this non-linear growth process. This establishes an empirical basis for using a Logistic S-Curve growth model for long-term forecasting in later sections.

\subsection{Cross-sectional Analysis of Car Ownership and EV Penetration}
To test the conventional assumption that "overall car ownership scale is positively correlated with EV adoption rates," this study comparatively analyzed overall car ownership rates and EV penetration data across regions for the year 2025.

% --- Figure 6.3 Placeholder ---
\begin{figure}[H]
    \centering
    \includegraphics[width=0.85\textwidth]{example-image}
    \caption{Cross-comparative chart of overall car ownership and EV penetration by region (2025)}
    \label{fig:car_ownership}
\end{figure}

Figure \ref{fig:car_ownership} illustrates the non-synergistic characteristics of some regions regarding these two indicators. Taking London as an example, its overall car ownership per thousand people (red bars) is at a lower level nationwide; however, its EV penetration rate (green line) reaches 10.8\%, which is relatively high. This cross-sectional feature suggests that, at the current stage, EV adoption does not strictly follow the scale distribution of traditional car ownership. Higher purchasing costs and specific commuting scenarios mean that EV consumption entails a certain economic selection threshold. This implies that future research should not rely solely on the absolute total number of vehicles as a core explanatory variable, but needs to further examine the practical impacts of wealth levels and supporting infrastructure.

\subsection{Baseline Correlation Testing of Economic Variables}
Based on the above findings, this study performed a univariate baseline scatter plot fitting for GDHI per head and EV penetration across regions in 2025.

% --- Figure 6.4 Placeholder ---
\begin{figure}[H]
    \centering
    \includegraphics[width=0.85\textwidth]{example-image}
    \caption{Linear trend chart of regional GDHI per head and EV penetration in 2025}
    \label{fig:gdhi_scatter}
\end{figure}

Figure \ref{fig:gdhi_scatter} shows an initial positive correlation trend between GDHI and EV penetration in major regions such as England, Scotland, and Wales. This verifies the leading driving role of economic levels in EV adoption. However, observing the dispersion of the scatter points reveals that a single income indicator cannot fully explain the variance in penetration rates. Since high-income regions generally also feature higher charging infrastructure density, a potential confounding effect exists between the two. This phenomenon highlights the limitations of direct univariate observation, thereby justifying the use of two-way panel fixed effects and machine learning models in the next section to isolate and quantify the true impact weights of income and infrastructure, respectively.

\subsection{Data Distribution Testing and Anomaly Identification}
To establish the foundational statistical characteristics of the prediction target and investigate extreme distribution samples, this study plotted a distribution histogram of EV penetration at the Local Authority District (LAD) level for 2025 and conducted scatter plot positioning analysis incorporating economic indicators.

\begin{figure}[H] % 使用 [H] 强制固定在此位置
    \centering

​    % --- 左侧第一张图 (Figure 6.5) ---
% minipage 宽度设为 0.48 倍正文宽度，留出 0.04 的间距
\begin{minipage}{0.48\textwidth}
​    \centering
​    % 图像宽度设为相对于 minipage 的 100%
​    % 上传真实图片后，请将 'example-image' 替换为您的文件名
​    \includegraphics[width=\textwidth]{example-image}
​    \caption{Distribution histogram of EV penetration at the UK Local Authority District (LAD) level (2025)}
​    \label{fig:histogram} % 保持原来的标签，方便文中引用
\end{minipage}
\hfill % 水平填充，自动撑开两图之间的距离
% --- 右侧第二张图 (Figure 6.6) ---
\begin{minipage}{0.48\textwidth}
​    \centering
​    % 上传真实图片后，请将 'example-image' 替换为您的文件名
​    \includegraphics[width=\textwidth]{example-image}
​    \caption{Scatter plot of anomaly samples deviating from the trend of income level and EV penetration (2023)}
​    \label{fig:anomaly} % 保持原来的标签
\end{minipage}

\end{figure}

The histogram in Figure \ref{fig:histogram} shows that EV penetration at the LAD level exhibits a distinct right-skewed distribution at the micro level (mean 6.60\% $>$ median 5.03\%), indicating that a small number of high-penetration regions inflate the overall average. Further observation of the scatter plot in Figure \ref{fig:anomaly} identifies certain special samples that deviate from the conventional "income-penetration" linear fitting trend. One group consists of the green highlighted points (e.g., Stockport, Peterborough), which achieved relatively high adoption rates despite lower economic baselines. The other group comprises the blue highlighted points (e.g., Kensington and Chelsea), which have high income levels but comparatively low adoption rates. The existence of these anomalous regions, which deviate from the overall trend, indicates that global linear fitting is susceptible to interference from individual extreme samples. This provides empirical support for subsequently introducing high-order machine learning models (such as XGBoost) that are capable of accommodating non-linear relationships.

\end{document}