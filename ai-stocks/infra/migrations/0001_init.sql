CREATE TABLE IF NOT EXISTS tickers (
  symbol text PRIMARY KEY,
  name text,
  sector text,
  industry text,
  pe numeric,
  peg numeric
);

CREATE TABLE IF NOT EXISTS prices (
  symbol text,
  ts timestamptz,
  o numeric, h numeric, l numeric, c numeric,
  v bigint,
  interval text DEFAULT '1d',
  PRIMARY KEY (symbol, ts, interval)
);

CREATE TABLE IF NOT EXISTS indicators (
  symbol text,
  ts timestamptz,
  squeeze_on boolean,
  squeeze_firing boolean,
  momentum numeric,
  breakout_55d boolean,
  near_breakout boolean,
  PRIMARY KEY (symbol, ts)
);

CREATE TABLE IF NOT EXISTS news (
  id text PRIMARY KEY,
  ts timestamptz,
  source text,
  symbol text,
  title text,
  url text
);

CREATE TABLE IF NOT EXISTS signals (
  id bigserial PRIMARY KEY,
  symbol text,
  ts timestamptz,
  kind text,
  payload jsonb
);
