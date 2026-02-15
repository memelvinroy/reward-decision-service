import http from 'k6/http';
import { check } from 'k6';

export const options = {
  scenarios: {
    constant_request_rate: {
      executor: 'constant-arrival-rate',
      rate: 300,          // 300 requests per second
      timeUnit: '1s',
      duration: '30s',
      preAllocatedVUs: 100,
      maxVUs: 300,
    },
  },
};

export default function () {
  const payload = JSON.stringify({
    txn_id: `t${__VU}-${__ITER}`,
    user_id: "user_new",
    merchant_id: "m1",
    amount: 100,
    txn_type: "ONLINE",
    ts: Date.now()
  });

  const params = {
    headers: { 'Content-Type': 'application/json' },
  };

  const res = http.post(
    'http://127.0.0.1:8000/reward/decide',
    payload,
    params
  );

  check(res, {
    'status 200': (r) => r.status === 200,
  });
}