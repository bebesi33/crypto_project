# Laszlo's crypto risk calculator : "crypto_project" repository

<p align="justify">This project serves as the basis of my BSc thesis in Computer Science.
In this project, I leverage my existing quailifications (Financial Mathematics) along with the knowledge I gained as part of the ELTE Computer Science BSc program.</p>

<h3><b> Overview </b></h3>

<p align="justify">
Since the invention of Bitcoin in 2008 (Nakamoto Satoshi, 2008), cryptocurrencies have become a new financial asset class. As of November 1st, 2024, there are around 10 thousand different cryptocurrencies available across the world, with approximately 3 Trillion USD in market capitalization (CoinMarketCap, 2024). Investors are tempted to choose this asset class, as many cryptocurrencies such as Bitcoin, Ethereum, or Binance have shown periods of high returns in recent times. Historically, there is also no strong correlation with traditional asset classes such as stocks or bonds, which helps investors diversify their portfolios. The decentralized nature of these assets can also be appealing to investors, as there is limited control over them from financial authorities.
Despite being a tempting investment alternative, the inherent risk in cryptocurrencies are seldom addressed. Namely, cryptocurrencies (even large ones like Ethereum or Bitcoin) are extremely volatile:  their annualized volatility can easily exceed 50 % (or in daily volatility 2.5 %), whereas stocks tend to have approximately 20 % annualized volatility, while annualized volatility of bonds seldom exceeds 10 %.</p>

<p align="justify">
The objective of this thesis is to implement a web-based application that can act as a risk calculation engine. The application will enable users to measure the risk of the cryptocurrency portfolios and will give opportunity to measure the risk of their portfolios during time periods of stress. It will also allow the users to identify the largest contributors of risks within their portfolios. To accomplish this, the application should interact with a financial risk model and utilize the risk model’s precalculated output. Users have two options to choose from: they can calculate their portfolio’s risk using a fundamental factor model with economically meaningful factors, or they can rely on simple calculations based on cryptocurrency excess returns time series co-movements. An important aspect of the problem that the application intends to solve is providing documentation on the financial mathematical background (for both calculation types), making this documentation an integral part of the application. The application is designed for cryptocurrency-only portfolios; however, if the underlying financial models are populated with data from other asset classes the application can accommodate other asset class types as well.
 </p>

<p align="justify">
From a technical perspective, the web-based client-server application is built using the Python-based Django framework. Django servers as a backend and as a database server for this application while the frontend utilizes the React.js JavaScript library. The databases used by the application are not managed by Django, meaning the server can only read from these tables, as the databases are expected to receive periodic updates from external sources.
</p>

<h3><b>Application Layout </b></h3>

<p align="justify">
After opening the application in a web browser, the user can use the navigation panel at the top of the page to access the Documentation, Explorer tool, and Risk Calculator. The main page also contains cards linking directly to the Explorer and Risk Calculator applications.
</p>
<p align="justify">
As a general principle, both the Explorer tool and Rick calculator tools use a control panel on the top left of the page, a message panel is provided for both tools. The message panel is either available on the top of the page or below the control panel. If a request is submitted the message panels are always populated. As the parametrization in many cases is not straight forward and requires financial knowledge, the message panel appears on the screen after every request. The background colour of the message panel can indicate the severity of the problems: blue indicates no caveats, yellow indicates caveats that do not prevent the calculations from starting, while red background indicates major issues that prevent risk calculation.
</p>

<h3><b> Screenshots </b></h3>

![image](https://github.com/user-attachments/assets/49a90f58-8fe9-4c42-bde8-c7d82db882bd)
<b> Explorer tool </b>
![image](https://github.com/user-attachments/assets/3bca9de3-fb4c-4cfe-a6df-a1311acb8390)
<b> Risk Calculator tool </b>
![image](https://github.com/user-attachments/assets/7e1c7e62-d72b-42cb-8d47-7479638b4180)

<b>Sources:</b>
<br>Nakamoto, Satoshi (31 October 2008). "Bitcoin: A Peer-to-Peer Electronic Cash System" (PDF). Accessed at [Link](https://bitcoin.org/bitcoin.pdf), 2024.11.15
<br>CointMarketCap (2024): Accessed at https://coinmarketcap.com/charts/ 2024.11.01.
