# B2B Inventory Sync Automation (RPA)

> **"From Manual Chaos to Fully Automated Sync"**
> *(수동 엑셀 작업의 100% 자동화 솔루션)*

## Project Overview
This project automates the daily inventory management workflow between a **B2B Supplier Portal** and an **E-commerce Store** (Shopify/WooCommerce).
It replaces the manual process of logging into a supplier's portal, downloading Excel files, and updating stock levels.

* **Target:** B2B Supplier Portal (Login required) & E-commerce Store.
* **Goal:** Zero manual data entry. Keep stock levels 100% accurate in real-time.
* **Impact:** Reduced daily workload by **2 hours** per day.

---

## Automation Architecture (How it Works)

```mermaid
graph TD
    %% Style Definitions / 스타일 정의
    classDef secret fill:#ffebee,stroke:#c62828,stroke-width:2px;
    classDef cloud fill:#e3f2fd,stroke:#1565c0,stroke-width:2px;
    classDef logic fill:#fff3e0,stroke:#ef6c00,stroke-width:2px;
    classDef ext fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px;
    classDef ops fill:#f3e5f5,stroke:#6a1b9a,stroke-width:2px;

    %% 1. Security Phase (보안 단계)
    GSM[Google Secret Manager<br/>(구글 시크릿 매니저)]:::secret -->|Load Secrets (no hardcode)<br/>(보안 키 로드)| Secrets[Secrets Cache (Memory)<br/>(메모리 캐시)]:::secret
    Secrets -.->|Inject Creds<br/>(자격증명 주입)| Bot

    %% 2. Core Logic (봇의 핵심 로직)
    subgraph "Python Automation Agent<br/>(파이썬 자동화 에이전트)"
        Bot[Main Controller<br/>(메인 컨트롤러)]:::logic
        Selenium[🕷️ Selenium Scraper<br/>(웹 수집기)]:::logic
        Pandas[Pandas ETL<br/>(데이터 가공)]:::logic
        Guard[Guard Logic: Retry/Rate Limit<br/>(안전장치: 재시도/API제한)]:::ops
        Evidence[Artifacts: Screenshot/HTML/Logs<br/>(증거 자료: 스샷/로그)]:::ops
    end

    %% 3. External Source Connection (외부 소스 연결)
    SnowXXXX[B2B Portal<br/>(B2B 포털)]:::ext -- Login & Download<br/>(로그인 및 다운로드) --> Selenium
    Selenium -- Error/Changes<br/>(에러/변경 감지) --> Evidence
    Selenium -- Excel/Raw Data<br/>(엑셀/원천 데이터) --> Pandas

    %% 4. DB Storage & Sync (DB 저장 및 동기화)
    Pandas -->|Write Validated Data<br/>(검증 데이터 저장)| DB[(Cloud SQL / PostgreSQL<br/>클라우드 DB)]:::cloud
    Bot -->|Read Mapping / Rules<br/>(매핑/룰 조회)| DB
    DB -->|Verified Data / State<br/>(검증 결과/상태)| Bot

    %% 5. Final Sync (Target Option) / 최종 반영
    Bot --> Guard
    Guard -- Update Inventory<br/>(재고 동기화) --> Shopify[Shopify Store<br/>(쇼피파이 스토어)]:::ext
    Guard -.->|OR (또는)| Woo[WooCommerce<br/>(우커머스)]:::ext

    %% 6. Notification (Slack & Email) / 알림
    Bot -- Report Result<br/>(결과 리포트) --> Notify[Slack / Email Alert<br/>(슬랙 및 이메일 알림)]:::ext
    Secrets -.->|Auth Token<br/>(인증 토큰)| Notify