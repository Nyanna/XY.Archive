-- =====================================================================
-- migration_optimize_storage.sql
-- Storage-Optimierung der Gadgetbridge-Postgres-Replik
-- Erstellt: 2026-04-27
-- =====================================================================
--
-- ZIEL
-- ---------------------------------------------------------------------
-- 1. bigint TIMESTAMP / TIMESTAMP_MS / WAKEUP_TIME ersatzlos droppen,
--    weil parallel timestamptz-Spalten (`<col>_at`) existieren und in
--    den Schreib- und Berechnungsskripten als kanonische Zeitachse
--    übernommen werden.
-- 2. PKs auf die `_at`-Spalte umziehen.
-- 3. bigint -> smallint Downcast für Skalar-Werte.
-- 4. double precision -> real für HRV-Aggregate.
-- 5. fillfactor=100 explizit setzen (Append-Only-Charakter).
--
-- IST-ZUSTAND (2026-04-27, ~663 MB Gesamt-DB-Größe)
-- ---------------------------------------------------------------------
-- table                           rows       heap     index    total
-- HEART_PULSE_SAMPLE              2.95M      169 MB   89 MB    258 MB
-- HEART_RR_INTERVAL_SAMPLE        1.46M      107 MB   57 MB    164 MB
-- BATTERY_LEVEL                   984k        64 MB   38 MB    102 MB
-- GENERIC_HEART_RATE_SAMPLE       1.04M       68 MB   31 MB     99 MB
-- XIAOMI_ACTIVITY_SAMPLE          153k        20 MB    5 MB     24 MB
-- (übrige Tabellen klein, mitmigriert ohne Größenrelevanz)
--
-- DATENKORREKTUR vor Drop
-- ---------------------------------------------------------------------
-- BATTERY_LEVEL."TIMESTAMP" ist in Sekunden (alle anderen Sample-
-- Tabellen in Millisekunden), wird aber von cleanup_gadgetbridge.py
-- in Version vor diesem Refactor mit ms_to_ts(TIMESTAMP/1000) in
-- timestamp_at umgerechnet -> timestamp_at zeigt fälschlich auf 1970.
-- Vor dem Drop wird timestamp_at neu aus TIMESTAMP berechnet
-- (to_timestamp(int) interpretiert Sekunden).
--
-- ERWARTETE EINSPARUNG (vs. 663 MB heute)
-- ---------------------------------------------------------------------
-- Drop bigint TS-Spalte:        ~ 5 M Rows × 8 B = ~ 40 MB heap
-- Schmaleres PK (TS aus PK weg): ~ 60 MB index (composite shrink)
-- Smallint-Downcasts:           ~ 100 MB heap
-- PK-Index-Shrink durch Smallint:~ 60 MB
-- HRV double->real:             ~ 1-2 MB
-- ---------------------------------------------------------------------
-- Summe Ziel:                   ~ 400 MB DB-Gesamt (-40 %)
--
-- HINWEIS
-- ---------------------------------------------------------------------
-- ALTER COLUMN TYPE rewrites die Tabelle (Heap + alle Indices) im
-- Ganzen. ACCESS EXCLUSIVE-Lock — in Wartungsfenster ausführen.
-- Benötigt temporär ~doppelten Tabellen-Speicherplatz.
-- =====================================================================

BEGIN;

-- =====================================================================
-- 0. BATTERY_LEVEL.timestamp_at reparieren (Sekunden statt Millisekunden)
-- =====================================================================
UPDATE public."BATTERY_LEVEL"
   SET timestamp_at = to_timestamp("TIMESTAMP")
 WHERE timestamp_at IS DISTINCT FROM to_timestamp("TIMESTAMP");

-- =====================================================================
-- 1. HEART_PULSE_SAMPLE
-- =====================================================================
ALTER TABLE public."HEART_PULSE_SAMPLE"
    DROP CONSTRAINT "HEART_PULSE_SAMPLE_pkey";
ALTER TABLE public."HEART_PULSE_SAMPLE"
    ALTER COLUMN timestamp_at SET NOT NULL,
    ALTER COLUMN "DEVICE_ID" TYPE smallint USING "DEVICE_ID"::smallint,
    ALTER COLUMN "USER_ID"   TYPE smallint USING "USER_ID"::smallint;
ALTER TABLE public."HEART_PULSE_SAMPLE"
    ADD CONSTRAINT "HEART_PULSE_SAMPLE_pkey"
    PRIMARY KEY (timestamp_at, "DEVICE_ID");
ALTER TABLE public."HEART_PULSE_SAMPLE" DROP COLUMN "TIMESTAMP";
ALTER TABLE public."HEART_PULSE_SAMPLE" SET (fillfactor = 100);

-- =====================================================================
-- 2. HEART_RR_INTERVAL_SAMPLE
-- =====================================================================
ALTER TABLE public."HEART_RR_INTERVAL_SAMPLE"
    DROP CONSTRAINT "HEART_RR_INTERVAL_SAMPLE_pkey";
ALTER TABLE public."HEART_RR_INTERVAL_SAMPLE"
    ALTER COLUMN timestamp_at SET NOT NULL,
    ALTER COLUMN "DEVICE_ID" TYPE smallint USING "DEVICE_ID"::smallint,
    ALTER COLUMN "USER_ID"   TYPE smallint USING "USER_ID"::smallint,
    ALTER COLUMN "SEQ"       TYPE smallint USING "SEQ"::smallint,
    ALTER COLUMN "RR_MILLIS" TYPE smallint USING "RR_MILLIS"::smallint;
ALTER TABLE public."HEART_RR_INTERVAL_SAMPLE"
    ADD CONSTRAINT "HEART_RR_INTERVAL_SAMPLE_pkey"
    PRIMARY KEY (timestamp_at, "DEVICE_ID", "SEQ");
ALTER TABLE public."HEART_RR_INTERVAL_SAMPLE" DROP COLUMN "TIMESTAMP";
ALTER TABLE public."HEART_RR_INTERVAL_SAMPLE" SET (fillfactor = 100);

-- =====================================================================
-- 3. BATTERY_LEVEL
-- =====================================================================
ALTER TABLE public."BATTERY_LEVEL"
    DROP CONSTRAINT "BATTERY_LEVEL_pkey";
ALTER TABLE public."BATTERY_LEVEL"
    ALTER COLUMN timestamp_at SET NOT NULL,
    ALTER COLUMN "DEVICE_ID"     TYPE smallint USING "DEVICE_ID"::smallint,
    ALTER COLUMN "LEVEL"         TYPE smallint USING "LEVEL"::smallint,
    ALTER COLUMN "BATTERY_INDEX" TYPE smallint USING "BATTERY_INDEX"::smallint;
ALTER TABLE public."BATTERY_LEVEL"
    ADD CONSTRAINT "BATTERY_LEVEL_pkey"
    PRIMARY KEY (timestamp_at, "DEVICE_ID", "BATTERY_INDEX");
ALTER TABLE public."BATTERY_LEVEL" DROP COLUMN "TIMESTAMP";
ALTER TABLE public."BATTERY_LEVEL" SET (fillfactor = 100);

-- =====================================================================
-- 4. GENERIC_HEART_RATE_SAMPLE
-- =====================================================================
ALTER TABLE public."GENERIC_HEART_RATE_SAMPLE"
    DROP CONSTRAINT "GENERIC_HEART_RATE_SAMPLE_pkey";
ALTER TABLE public."GENERIC_HEART_RATE_SAMPLE"
    ALTER COLUMN timestamp_at SET NOT NULL,
    ALTER COLUMN "DEVICE_ID"  TYPE smallint USING "DEVICE_ID"::smallint,
    ALTER COLUMN "USER_ID"    TYPE smallint USING "USER_ID"::smallint,
    ALTER COLUMN "HEART_RATE" TYPE smallint USING "HEART_RATE"::smallint;
ALTER TABLE public."GENERIC_HEART_RATE_SAMPLE"
    ADD CONSTRAINT "GENERIC_HEART_RATE_SAMPLE_pkey"
    PRIMARY KEY (timestamp_at, "DEVICE_ID");
ALTER TABLE public."GENERIC_HEART_RATE_SAMPLE" DROP COLUMN "TIMESTAMP";
ALTER TABLE public."GENERIC_HEART_RATE_SAMPLE" SET (fillfactor = 100);

-- =====================================================================
-- 5. XIAOMI_ACTIVITY_SAMPLE
-- =====================================================================
ALTER TABLE public."XIAOMI_ACTIVITY_SAMPLE"
    DROP CONSTRAINT "XIAOMI_ACTIVITY_SAMPLE_pkey";
ALTER TABLE public."XIAOMI_ACTIVITY_SAMPLE"
    ALTER COLUMN timestamp_at SET NOT NULL,
    ALTER COLUMN "DEVICE_ID"       TYPE smallint USING "DEVICE_ID"::smallint,
    ALTER COLUMN "USER_ID"         TYPE smallint USING "USER_ID"::smallint,
    ALTER COLUMN "RAW_INTENSITY"   TYPE smallint USING "RAW_INTENSITY"::smallint,
    ALTER COLUMN "STEPS"           TYPE smallint USING "STEPS"::smallint,
    ALTER COLUMN "RAW_KIND"        TYPE smallint USING "RAW_KIND"::smallint,
    ALTER COLUMN "HEART_RATE"      TYPE smallint USING "HEART_RATE"::smallint,
    ALTER COLUMN "STRESS"          TYPE smallint USING "STRESS"::smallint,
    ALTER COLUMN "SPO2"            TYPE smallint USING "SPO2"::smallint,
    ALTER COLUMN "ACTIVE_CALORIES" TYPE smallint USING "ACTIVE_CALORIES"::smallint,
    ALTER COLUMN "DISTANCE_CM"     TYPE smallint USING "DISTANCE_CM"::smallint,
    ALTER COLUMN "ENERGY"          TYPE smallint USING "ENERGY"::smallint;
ALTER TABLE public."XIAOMI_ACTIVITY_SAMPLE"
    ADD CONSTRAINT "XIAOMI_ACTIVITY_SAMPLE_pkey"
    PRIMARY KEY (timestamp_at, "DEVICE_ID");
ALTER TABLE public."XIAOMI_ACTIVITY_SAMPLE" DROP COLUMN "TIMESTAMP";
ALTER TABLE public."XIAOMI_ACTIVITY_SAMPLE" SET (fillfactor = 100);

-- =====================================================================
-- 6. Kleine Sample-Tabellen
-- =====================================================================
ALTER TABLE public."XIAOMI_SLEEP_STAGE_SAMPLE"
    DROP CONSTRAINT "XIAOMI_SLEEP_STAGE_SAMPLE_pkey";
ALTER TABLE public."XIAOMI_SLEEP_STAGE_SAMPLE"
    ALTER COLUMN timestamp_at SET NOT NULL,
    ALTER COLUMN "DEVICE_ID" TYPE smallint USING "DEVICE_ID"::smallint,
    ALTER COLUMN "USER_ID"   TYPE smallint USING "USER_ID"::smallint,
    ALTER COLUMN "STAGE"     TYPE smallint USING "STAGE"::smallint;
ALTER TABLE public."XIAOMI_SLEEP_STAGE_SAMPLE"
    ADD CONSTRAINT "XIAOMI_SLEEP_STAGE_SAMPLE_pkey"
    PRIMARY KEY (timestamp_at, "DEVICE_ID");
ALTER TABLE public."XIAOMI_SLEEP_STAGE_SAMPLE" DROP COLUMN "TIMESTAMP";

ALTER TABLE public."XIAOMI_MANUAL_SAMPLE"
    DROP CONSTRAINT "XIAOMI_MANUAL_SAMPLE_pkey";
ALTER TABLE public."XIAOMI_MANUAL_SAMPLE"
    ALTER COLUMN timestamp_at SET NOT NULL,
    ALTER COLUMN "DEVICE_ID" TYPE smallint USING "DEVICE_ID"::smallint,
    ALTER COLUMN "USER_ID"   TYPE smallint USING "USER_ID"::smallint,
    ALTER COLUMN "TYPE"      TYPE smallint USING "TYPE"::smallint,
    ALTER COLUMN "VALUE"     TYPE smallint USING "VALUE"::smallint;
ALTER TABLE public."XIAOMI_MANUAL_SAMPLE"
    ADD CONSTRAINT "XIAOMI_MANUAL_SAMPLE_pkey"
    PRIMARY KEY (timestamp_at, "DEVICE_ID");
ALTER TABLE public."XIAOMI_MANUAL_SAMPLE" DROP COLUMN "TIMESTAMP";

ALTER TABLE public."XIAOMI_SLEEP_TIME_SAMPLE"
    DROP CONSTRAINT "XIAOMI_SLEEP_TIME_SAMPLE_pkey";
ALTER TABLE public."XIAOMI_SLEEP_TIME_SAMPLE"
    ALTER COLUMN timestamp_at SET NOT NULL,
    ALTER COLUMN "DEVICE_ID" TYPE smallint USING "DEVICE_ID"::smallint,
    ALTER COLUMN "USER_ID"   TYPE smallint USING "USER_ID"::smallint,
    ALTER COLUMN "IS_AWAKE"  TYPE smallint USING "IS_AWAKE"::smallint;
ALTER TABLE public."XIAOMI_SLEEP_TIME_SAMPLE"
    ADD CONSTRAINT "XIAOMI_SLEEP_TIME_SAMPLE_pkey"
    PRIMARY KEY (timestamp_at, "DEVICE_ID");
-- WAKEUP_TIME hat bereits wakeup_time_at, ebenfalls überflüssig:
ALTER TABLE public."XIAOMI_SLEEP_TIME_SAMPLE" DROP COLUMN "TIMESTAMP";
ALTER TABLE public."XIAOMI_SLEEP_TIME_SAMPLE" DROP COLUMN "WAKEUP_TIME";

ALTER TABLE public."XIAOMI_DAILY_SUMMARY_SAMPLE"
    DROP CONSTRAINT "XIAOMI_DAILY_SUMMARY_SAMPLE_pkey";
ALTER TABLE public."XIAOMI_DAILY_SUMMARY_SAMPLE"
    ALTER COLUMN timestamp_at SET NOT NULL,
    ALTER COLUMN "DEVICE_ID"   TYPE smallint USING "DEVICE_ID"::smallint,
    ALTER COLUMN "USER_ID"     TYPE smallint USING "USER_ID"::smallint,
    ALTER COLUMN "TIMEZONE"    TYPE integer  USING "TIMEZONE"::integer,
    ALTER COLUMN "HR_RESTING"  TYPE smallint USING "HR_RESTING"::smallint,
    ALTER COLUMN "HR_MAX"      TYPE smallint USING "HR_MAX"::smallint,
    ALTER COLUMN "HR_MIN"      TYPE smallint USING "HR_MIN"::smallint,
    ALTER COLUMN "HR_AVG"      TYPE smallint USING "HR_AVG"::smallint,
    ALTER COLUMN "STRESS_AVG"  TYPE smallint USING "STRESS_AVG"::smallint,
    ALTER COLUMN "STRESS_MAX"  TYPE smallint USING "STRESS_MAX"::smallint,
    ALTER COLUMN "STRESS_MIN"  TYPE smallint USING "STRESS_MIN"::smallint,
    ALTER COLUMN "SPO2_MAX"    TYPE smallint USING "SPO2_MAX"::smallint,
    ALTER COLUMN "SPO2_MIN"    TYPE smallint USING "SPO2_MIN"::smallint,
    ALTER COLUMN "SPO2_AVG"    TYPE smallint USING "SPO2_AVG"::smallint;
ALTER TABLE public."XIAOMI_DAILY_SUMMARY_SAMPLE"
    ADD CONSTRAINT "XIAOMI_DAILY_SUMMARY_SAMPLE_pkey"
    PRIMARY KEY (timestamp_at, "DEVICE_ID");
ALTER TABLE public."XIAOMI_DAILY_SUMMARY_SAMPLE" DROP COLUMN "TIMESTAMP";
-- HR_MAX_TS / HR_MIN_TS / SPO2_MAX_TS / SPO2_MIN_TS bleiben bigint:
-- Keine `_at`-Konvertierung im Replikator vorhanden (kein _TS-Pattern).

-- =====================================================================
-- 7. HRV-Aggregat-Tabellen: bigint TIMESTAMP_MS droppen, double->real
-- =====================================================================
ALTER TABLE public."HRV_MINUTE_AGGREGATED"
    DROP CONSTRAINT "HRV_MINUTE_AGGREGATED_pkey";
ALTER TABLE public."HRV_MINUTE_AGGREGATED"
    ALTER COLUMN timestamp_ms_at SET NOT NULL,
    ALTER COLUMN "N_BEATS"          TYPE smallint USING "N_BEATS"::smallint,
    ALTER COLUMN "MIN_RR_MS"        TYPE smallint USING "MIN_RR_MS"::smallint,
    ALTER COLUMN "MAX_RR_MS"        TYPE smallint USING "MAX_RR_MS"::smallint,
    ALTER COLUMN "HR_BPM"           TYPE real USING "HR_BPM"::real,
    ALTER COLUMN "AVG_RR_MS"        TYPE real USING "AVG_RR_MS"::real,
    ALTER COLUMN "STDDEV_RR_MS"     TYPE real USING "STDDEV_RR_MS"::real,
    ALTER COLUMN "RMSSD_MS"         TYPE real USING "RMSSD_MS"::real,
    ALTER COLUMN "LN_RMSSD"         TYPE real USING "LN_RMSSD"::real,
    ALTER COLUMN "VAGAL_INDEX"      TYPE real USING "VAGAL_INDEX"::real,
    ALTER COLUMN "RMSSD_PCT"        TYPE real USING "RMSSD_PCT"::real,
    ALTER COLUMN "SDNN_MS"          TYPE real USING "SDNN_MS"::real,
    ALTER COLUMN "RMSSD_SDNN_RATIO" TYPE real USING "RMSSD_SDNN_RATIO"::real,
    ALTER COLUMN "VAGAL_BALANCE"    TYPE real USING "VAGAL_BALANCE"::real,
    ALTER COLUMN "PNN50"            TYPE real USING "PNN50"::real,
    ALTER COLUMN "VLF_MS2"          TYPE real USING "VLF_MS2"::real,
    ALTER COLUMN "LF_MS2"           TYPE real USING "LF_MS2"::real,
    ALTER COLUMN "HF_MS2"           TYPE real USING "HF_MS2"::real,
    ALTER COLUMN "ULF_MS2"          TYPE real USING "ULF_MS2"::real,
    ALTER COLUMN "ULF1_MS2"         TYPE real USING "ULF1_MS2"::real,
    ALTER COLUMN "ULF2_MS2"         TYPE real USING "ULF2_MS2"::real,
    ALTER COLUMN "LF_HF_RATIO"      TYPE real USING "LF_HF_RATIO"::real,
    ALTER COLUMN "B7B8_DOM"         TYPE real USING "B7B8_DOM"::real,
    ALTER COLUMN "B7B8_OFF"         TYPE real USING "B7B8_OFF"::real,
    ALTER COLUMN "DFA_ALPHA1"       TYPE real USING "DFA_ALPHA1"::real;
ALTER TABLE public."HRV_MINUTE_AGGREGATED"
    ADD CONSTRAINT "HRV_MINUTE_AGGREGATED_pkey"
    PRIMARY KEY (timestamp_ms_at);
ALTER TABLE public."HRV_MINUTE_AGGREGATED" DROP COLUMN "TIMESTAMP_MS";
ALTER TABLE public."HRV_MINUTE_AGGREGATED" SET (fillfactor = 100);

ALTER TABLE public."HRV_SPECTRAL_BANDS_MINUTE"
    DROP CONSTRAINT "HRV_SPECTRAL_BANDS_MINUTE_pkey";
ALTER TABLE public."HRV_SPECTRAL_BANDS_MINUTE"
    ALTER COLUMN timestamp_ms_at SET NOT NULL,
    ALTER COLUMN "N_BEATS"      TYPE smallint USING "N_BEATS"::smallint,
    ALTER COLUMN "CIRC_24H"     TYPE real USING "CIRC_24H"::real,
    ALTER COLUMN "CIRC_11H"     TYPE real USING "CIRC_11H"::real,
    ALTER COLUMN "CIRC_6H"      TYPE real USING "CIRC_6H"::real,
    ALTER COLUMN "CIRC_5H"      TYPE real USING "CIRC_5H"::real,
    ALTER COLUMN "CIRC_4H"      TYPE real USING "CIRC_4H"::real,
    ALTER COLUMN "ULF_22MIN"    TYPE real USING "ULF_22MIN"::real,
    ALTER COLUMN "ULF_10MIN"    TYPE real USING "ULF_10MIN"::real,
    ALTER COLUMN "ULF_8MIN"     TYPE real USING "ULF_8MIN"::real,
    ALTER COLUMN "VLF_5MIN"     TYPE real USING "VLF_5MIN"::real,
    ALTER COLUMN "VLF_4MIN"     TYPE real USING "VLF_4MIN"::real,
    ALTER COLUMN "LF_MAYER_10S" TYPE real USING "LF_MAYER_10S"::real,
    ALTER COLUMN "HF_BREATH_5S" TYPE real USING "HF_BREATH_5S"::real,
    ALTER COLUMN "HF_BREATH_4S" TYPE real USING "HF_BREATH_4S"::real,
    ALTER COLUMN "HF_BREATH_3S" TYPE real USING "HF_BREATH_3S"::real,
    ALTER COLUMN "HF_BREATH_2S" TYPE real USING "HF_BREATH_2S"::real;
ALTER TABLE public."HRV_SPECTRAL_BANDS_MINUTE"
    ADD CONSTRAINT "HRV_SPECTRAL_BANDS_MINUTE_pkey"
    PRIMARY KEY (timestamp_ms_at);
ALTER TABLE public."HRV_SPECTRAL_BANDS_MINUTE" DROP COLUMN "TIMESTAMP_MS";
ALTER TABLE public."HRV_SPECTRAL_BANDS_MINUTE" SET (fillfactor = 100);

COMMIT;

-- =====================================================================
-- 8. Statistik-Refresh und Speicher-Reclaim nach DROP COLUMN
-- =====================================================================
-- DROP COLUMN markiert die Spalte intern nur als gelöscht; physischer
-- Speicher wird erst durch Heap-Rewrite freigegeben. Die ALTER COLUMN
-- TYPE-Statements oben haben jede Tabelle bereits neu geschrieben, so
-- dass die gedroppten Spalten effektiv nicht mehr im Heap stehen.
-- ANALYSE für aktuelle Planner-Statistiken:
ANALYZE public."HEART_PULSE_SAMPLE";
ANALYZE public."HEART_RR_INTERVAL_SAMPLE";
ANALYZE public."BATTERY_LEVEL";
ANALYZE public."GENERIC_HEART_RATE_SAMPLE";
ANALYZE public."XIAOMI_ACTIVITY_SAMPLE";
ANALYZE public."XIAOMI_SLEEP_STAGE_SAMPLE";
ANALYZE public."XIAOMI_MANUAL_SAMPLE";
ANALYZE public."XIAOMI_SLEEP_TIME_SAMPLE";
ANALYZE public."XIAOMI_DAILY_SUMMARY_SAMPLE";
ANALYZE public."HRV_MINUTE_AGGREGATED";
ANALYZE public."HRV_SPECTRAL_BANDS_MINUTE";

-- =====================================================================
-- 9. Verifikation
-- =====================================================================
-- SELECT
--     c.relname,
--     pg_size_pretty(pg_total_relation_size(c.oid)) AS total,
--     pg_size_pretty(pg_relation_size(c.oid))       AS heap,
--     pg_size_pretty(pg_indexes_size(c.oid))        AS idx
-- FROM pg_class c
-- JOIN pg_namespace n ON n.oid = c.relnamespace
-- WHERE c.relkind='r' AND n.nspname='public'
-- ORDER BY pg_total_relation_size(c.oid) DESC;
