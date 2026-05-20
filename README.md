# Telegram Bot QA Automation System (n8n + AI + Google Sheets)


## Problem Statement (Motivation)

## 🎥 Demo
https://drive.google.com/file/d/1Br658t0SE8S6YSriAlbGLpmBbxFa3DxH/view?usp=drive_link


A typical QA cycle looks like this:
- prepare a list of test questions
- manually send each message to the bot in Telegram
- wait for the bot response
- compare response with expected result
- log the outcome

This process is time-consuming, repetitive, and does not scale well when the number of test cases grows.

To solve this, the testing process was automated using **n8n workflows, Python Telegram client, and AI-based evaluation**.

The goal was to:
- remove manual interaction from QA testing
- ensure consistent and repeatable test execution
- introduce structured evaluation of chatbot responses
- speed up regression testing for Telegram bots

---

## Overview

This project is an automated QA system for testing Telegram chatbots.

It replaces manual chatbot testing with a structured pipeline that:

- sends predefined test cases to a Telegram bot
- captures bot responses via a user Telegram session
- evaluates responses using an LLM-based judge
- stores results in Google Sheets

The system is designed for black-box testing of chatbot behavior.

---

## Architecture

The system consists of two independent workflows:

---

## 1. Test Execution Workflow (Sender)

Responsible for sending test cases to the Telegram bot.

### Flow

- Reads test cases from Google Sheets
- Selects the next unsent test case
- Sends message to Telegram bot via HTTP request (Python Telegram client)
- Marks test as sent with timestamp (`SENDED`)
- Ensures sequential execution (one test at a time)

---

### Test Case Structure

Each test case contains:

- `TEST#` - unique test identifier
- `TYPE` - test category (edge case, injection, normal flow, etc.)
- `MESSAGE` - input message sent to bot
- `EXPECTED_RESULT` - expected bot behavior

---

### Execution Model

- Runs on a 15-second interval
- Prevents sending next message until current test is processed
- Simulates real user interaction timing

---

## 2. Response Capture + AI Evaluation Workflow (Judge)

Responsible for capturing bot responses and evaluating them.

### Flow

- Listens to Telegram via Python Telegram client (user session)
- Detects responses from the tested bot
- Writes actual response into Google Sheets (`ACTUAL_RESULT`)
- Triggers AI evaluation process

---

### AI Evaluation Input

- User message
- Expected result
- Actual bot response

---

### AI Output

- `STATUS: PASS | FAIL`
- `REASON: explanation of evaluation`

---

## Data Storage (Google Sheets)

Google Sheets is used as a lightweight QA database.

Each row represents a full test lifecycle:

- `TEST#` - test identifier
- `TYPE` - test category
- `MESSAGE` - input message
- `EXPECTED_RESULT` - expected behavior
- `SENDED` - timestamp when message was sent
- `ACTUAL_RESULT` - bot response
- `RESULT` - AI evaluation output

---

## Execution Flow

1. Test cases are defined in Google Sheets
2. Sender workflow selects next test case
3. Message is sent to Telegram bot via user session
4. Bot response is received in Telegram
5. Listener captures response and writes it to Google Sheets
6. AI judge evaluates response
7. Result is stored back in Google Sheets

---

## Supported Test Types

The system supports:

- normal conversation flows
- edge cases
- prompt injection attempts
- negative testing scenarios
- expected behavior validation cases

---

## Key Design Principles

- Black-box testing approach (no access to internal bot logic required)
- Sequential execution to avoid race conditions
- User-session-based Telegram interaction (not bot-only API)
- Google Sheets as external state storage
- AI-based evaluation for scalable QA decisions

---

## Tech Stack

```bash
n8n
Python Telegram Client
Google Sheets API
OpenAI GPT (LLM Judge)
HTTP Server (message dispatch)
