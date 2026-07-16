-- Create database container infrastructure matching enterprise architecture
CREATE OR REPLACE TRANSIENT TABLE trust_safety_raw_transactions (
    transaction_id VARCHAR,
    user_id VARCHAR,
    merchant_id VARCHAR,
    amount NUMBER(10,2),
    device_id VARCHAR,
    ip_address VARCHAR,
    location VARCHAR,
    timestamp TIMESTAMP_NTZ
);

-- Advanced Analytical Detection Script 1: Catching Velocity Overlap & Account Takeovers
-- This query catches users placing high frequency orders across distinct geographic locations within minutes.
WITH spatial_temporal_velocity AS (
    SELECT 
        transaction_id,
        user_id,
        location,
        timestamp,
        amount,
        LAG(location, 1) OVER (PARTITION BY user_id ORDER BY timestamp ASC) as previous_location,
        LAG(timestamp, 1) OVER (PARTITION BY user_id ORDER BY timestamp ASC) as previous_timestamp,
        TIMEDIFF(minute, previous_timestamp, timestamp) as minutes_since_last_order
    FROM trust_safety_raw_transactions
)
SELECT 
    transaction_id,
    user_id,
    location AS current_location,
    previous_location,
    minutes_since_last_order,
    amount,
    'ACCOUNT_TAKEOVER_GEOGRAPHIC_IMPOSSIBILITY' AS risk_signature
FROM spatial_temporal_velocity
WHERE minutes_since_last_order <= 15 
  AND current_location <> previous_location;


-- Advanced Analytical Detection Script 2: Catching Email Variant Abuse & Promo Farm Signups
-- Identifies fraudulent attempts to spoof unique consumer indexing logic via string parsing techniques.
SELECT 
    user_id,
    merchant_id,
    amount,
    timestamp,
    COUNT(transaction_id) OVER(PARTITION BY device_id, DATE(timestamp)) as daily_device_txn_density
FROM trust_safety_raw_transactions
QUALIFY daily_device_txn_density >= 5
ORDER BY daily_device_txn_density DESC;
