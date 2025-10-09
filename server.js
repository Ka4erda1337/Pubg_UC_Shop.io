import express from 'express';
import fs from 'fs';
import axios from 'axios';
const app = express();
const PORT = 3000;
const DB = './payments.json';

// настройки Tinkoff
const TINKOFF = {
  TerminalKey: process.env.TINKOFF_TERMINAL || '',
  Password: process.env.TINKOFF_PASSWORD || '',
  baseUrl: 'https://securepay.tinkoff.ru'
};

app.use(express.json());
app.use(express.static('.'));

// создать платёж
app.post('/api/create-payment', async (req, res) => {
  const { amount } = req.body;
  const orderId = Date.now().toString();

  try {
    let paymentUrl, qrData;

    if (!TINKOFF.TerminalKey || !TINKOFF.Password) {
      // тестовый QR
      paymentUrl = 'https://www.tinkoff.ru';
      qrData = paymentUrl + '?amount=' + amount;
    } else {
      const body = {
        TerminalKey: TINKOFF.TerminalKey,
        Amount: Math.round(parseFloat(amount) * 100),
        OrderId: orderId,
        Description: 'Оплата PUBG UC',
        PayType: 'SBP'
      };
      const resp = await axios.post(`${TINKOFF.baseUrl}/v2/Init`, body);
      if (resp.data.Success) {
        paymentUrl = resp.data.PaymentURL;
        qrData = resp.data.qrData || paymentUrl;
      } else {
        return res.status(500).json({ error: 'Ошибка от Tinkoff: ' + JSON.stringify(resp.data) });
      }
    }

    const payment = { id: orderId, amount, status: 'NEW', payUrl: paymentUrl, qrData };
    let db = [];
    if (fs.existsSync(DB)) db = JSON.parse(fs.readFileSync(DB, 'utf8'));
    db.push(payment);
    fs.writeFileSync(DB, JSON.stringify(db, null, 2));

    res.json({ paymentId: orderId, qrData, payUrl: paymentUrl });
  } catch (e) {
    console.error(e);
    res.status(500).json({ error: 'Ошибка при создании платежа' });
  }
});

// проверка статуса
app.get('/api/check-payment/:id', async (req, res) => {
  const id = req.params.id;
  let db = [];
  if (fs.existsSync(DB)) db = JSON.parse(fs.readFileSync(DB, 'utf8'));
  const payment = db.find(x => x.id === id);
  if (!payment) return res.json({ status: 'NOT_FOUND' });

  if (TINKOFF.TerminalKey && TINKOFF.Password) {
    try {
      const resp = await axios.post(`${TINKOFF.baseUrl}/v2/GetState`, {
        TerminalKey: TINKOFF.TerminalKey,
        OrderId: id
      });
      if (resp.data.Status) {
        payment.status = resp.data.Status;
        fs.writeFileSync(DB, JSON.stringify(db, null, 2));
        return res.json({ status: payment.status });
      }
    } catch (e) {
      console.error(e);
    }
  }

  // тестовый сценарий — через 20 сек платёж "прошёл"
  if (Date.now() - parseInt(id) > 20000) {
    payment.status = 'CONFIRMED';
    fs.writeFileSync(DB, JSON.stringify(db, null, 2));
  }
  res.json({ status: payment.status });
});

app.listen(PORT, () => console.log(`Server running on http://localhost:${PORT}`));
