ORCHESTRATE_AGENT_SYSTEM_PROMPT = """
[Persona]
You are a Ticket Handling Agent.

[Logic Rules]
- Ticket Type is generated based on Possibility percentage.
- Ticket Status must follow these rules:
  - Possibility ≤ 15%  → Normal
  - Possibility > 15% and ≤ 30% → HIGH
  - Possibility > 30% → ATTACK

[Instructions]
1. Generate ticket data dynamically.
2. Replace ALL placeholders in the HTML template.
3. Do NOT keep any static or example values.
4. Return ONLY valid HTML.
5. Do NOT include explanations, comments, or markdown.

[HTML Template With Placeholders]
<table border="1">
  <tr>
    <th>Ticket Type</th>
    <th>Possibility</th>
    <th>Ticket Status</th>
  </tr>
  <tr>
    <td>TICKET_TYPE</td>
    <td>POSSIBILITY%</td>
    <td>TICKET_STATUS</td>
  </tr>
</table>
"""

INPUT =""""


2026-02-07 10:15:01 INFO  203.0.113.12   GET  /home          200  120ms
2026-02-07 10:15:02 INFO  198.51.100.45  GET  /products      200  145ms
2026-02-07 10:15:03 INFO  192.0.2.88     POST /login         302  180ms
2026-02-07 10:15:04 INFO  203.0.113.67   GET  /dashboard     200  210ms
2026-02-07 10:15:05 INFO  198.51.100.19  GET  /profile       200  165ms
2026-02-07 10:15:06 INFO  192.0.2.101    GET  /orders        200  195ms
2026-02-07 10:15:07 INFO  203.0.113.34   GET  /logout        200  110ms
2026-02-07 10:15:08 INFO  198.51.100.77  GET  /contact       200  130ms



"""

Addition_Agent = """
You are a helpful and caring sister.
You assist your brother by using appropriate tools to generate clear, accurate, and supportive responses.
Always be polite, friendly, and easy to understand.
"""


Tool_Call_Input=""""
hey hamma hamma hamma hamma this music from where sister 
"""


Team_Agent="""
You are Sister, the manager agent.

STRICT RULES:
1. You must classify the user's request into ONE of these categories:
   - GENERAL
   - MATH
   - SONG

2. You are allowed to delegate to ONLY ONE team member.
3. You must NOT delegate more than once.
4. After receiving the response from that team member, you must immediately return the final answer.
5. Do NOT create additional plans.
6. Do NOT call multiple agents.
7. Do NOT re-delegate.

Delegation Rules:
- If the request involves numbers or calculations → delegate to Math Teacher.
- If the request involves song or lyrics → delegate to Spotify.
- Otherwise → respond directly yourself.

You must follow these rules strictly.
"""



ITSM_AGENT_SYSTEM_PROMPT = """
[Persona]
You are an Intelligent ITSM Orchestrator Agent.

Your responsibility is to coordinate specialized agents to handle IT incidents professionally.

[Available Agents]
1. Incident_Analyzer → Understands and classifies the incident.
2. Ticket_Creation → Generates structured ITSM ticket details.
3. Root_Cause_Analysis → Identifies probable technical root causes.
4. Resolution_Discovery → Suggests resolution steps from knowledge base.
5. General Agent → Handles non-incident generic queries.

[Strict Orchestration Rules]
1. Always start by sending the user input to Incident_Analyzer.
2. If the input is NOT an IT incident, delegate ONLY to General Agent and stop.
3. If the input IS an IT incident, follow this EXACT workflow:

   Step 1 → Incident_Analyzer
   Step 2 → Ticket_Creation
   Step 3 → Root_Cause_Analysis
   Step 4 → Resolution_Discovery

4. Execute agents in sequence.
5. Do NOT skip steps.
6. Do NOT repeat steps.
7. Do NOT call multiple agents simultaneously.
8. Do NOT create your own answers.

[Final Output Rules]
- Combine outputs from all executed agents.
- Return a structured ITSM report.
- Do NOT include explanations.
- Do NOT include markdown.
- Return only the final structured response.
- if Tickets created provide the ticket Id 
"""
LOG_503="""
192.168.1.45 - - [12/Feb/2026:10:15:23 +0000] "GET /api/v1/users HTTP/1.1" 503 182 "-" "Mozilla/5.0"
192.168.1.78 - - [12/Feb/2026:10:15:24 +0000] "POST /login HTTP/1.1" 503 210 "-" "Mozilla/5.0"
10.0.0.23 - - [12/Feb/2026:10:15:26 +0000] "GET /dashboard HTTP/1.1" 503 198 "-" "Chrome/120.0"
172.16.0.12 - - [12/Feb/2026:10:15:28 +0000] "GET /api/v1/orders HTTP/1.1" 503 175 "-" "PostmanRuntime/7.36.0"
203.0.113.9 - - [12/Feb/2026:10:15:30 +0000] "PUT /api/v1/profile HTTP/1.1" 503 220 "-" "Mozilla/5.0"

"""
APPACHEE_LOG ="""
i am system admin i am getting 

[Wed Feb 12 10:15:23.456789 2026] [proxy:error] [pid 2345] (111)Connection refused: AH00957: HTTP: attempt to connect to 127.0.0.1:8000 failed
[Wed Feb 12 10:15:23.456812 2026] [proxy_http:error] [pid 2345] AH01114: HTTP: failed to make connection to backend: 127.0.0.1
[Wed Feb 12 10:15:23.456830 2026] [core:error] [pid 2345] [client 192.168.1.45:54321] AH00124: Request exceeded the limit of 10 internal redirects due to probable configuration error.

"""
DDOS_LOGS = """

i am yoga getting this errors on my web server

1.  [2026-02-12 10:00:01] | 45.67.12.101 | GET  | /login              | 200 | 512  | Normal Request
2.  [2026-02-12 10:00:02] | 103.45.78.23 | GET  | /api/data           | 200 | 1024 | Normal Request
3.  [2026-02-12 10:00:03] | 185.23.44.91 | GET  | /                   | 200 | 2048 | Normal Request
4.  [2026-02-12 10:00:04] | 192.168.1.10 | POST | /login              | 200 | 768  | Normal Login
5.  [2026-02-12 10:00:05] | 10.0.0.5     | GET  | /dashboard          | 200 | 1500 | Internal User

6.  [2026-02-12 10:00:06] | 203.112.45.67 | GET  | /api/auth           | 503 | 0    | Suspicious High Rate
7.  [2026-02-12 10:00:06] | 203.112.45.68 | GET  | /api/auth           | 503 | 0    | Suspicious High Rate
8.  [2026-02-12 10:00:07] | 203.112.45.69 | GET  | /api/auth           | 503 | 0    | Suspicious High Rate
9.  [2026-02-12 10:00:07] | 203.112.45.70 | GET  | /api/auth           | 503 | 0    | Suspicious High Rate
10. [2026-02-12 10:00:08] | 203.112.45.71 | GET  | /api/auth           | 503 | 0    | Suspicious High Rate

11. [2026-02-12 10:00:08] | 91.34.55.201  | POST | /login              | 429 | 0    | Rate Limit Exceeded
12. [2026-02-12 10:00:09] | 91.34.55.202  | POST | /login              | 429 | 0    | Rate Limit Exceeded
13. [2026-02-12 10:00:09] | 91.34.55.203  | POST | /login              | 429 | 0    | Rate Limit Exceeded
14. [2026-02-12 10:00:10] | 91.34.55.204  | POST | /login              | 429 | 0    | Rate Limit Exceeded
15. [2026-02-12 10:00:10] | 91.34.55.205  | POST | /login              | 429 | 0    | Rate Limit Exceeded

16. [2026-02-12 10:00:11] | 172.16.4.12   | GET  | /health             | 200 | 256  | Monitoring
17. [2026-02-12 10:00:12] | 45.89.23.150  | GET  | /                   | 200 | 2048 | Normal Request
18. [2026-02-12 10:00:13] | 102.54.78.200 | GET  | /products           | 200 | 4096 | Normal User
19. [2026-02-12 10:00:14] | 178.23.90.111 | GET  | /api/search?q=test  | 200 | 1300 | Normal Query
20. [2026-02-12 10:00:15] | 150.12.34.88  | GET  | /contact            | 200 | 800  | Normal Request

21. [2026-02-12 10:00:16] | 210.45.66.10  | GET  | /api/auth           | 503 | 0    | DDoS Traffic
22. [2026-02-12 10:00:16] | 210.45.66.11  | GET  | /api/auth           | 503 | 0    | DDoS Traffic
23. [2026-02-12 10:00:17] | 210.45.66.12  | GET  | /api/auth           | 503 | 0    | DDoS Traffic
24. [2026-02-12 10:00:17] | 210.45.66.13  | GET  | /api/auth           | 503 | 0    | DDoS Traffic
25. [2026-02-12 10:00:18] | 210.45.66.14  | GET  | /api/auth           | 503 | 0    | DDoS Traffic

26. [2026-02-12 10:00:18] | 66.77.88.99   | GET  | /api/payment        | 500 | 0    | Server Overload
27. [2026-02-12 10:00:19] | 66.77.88.100  | GET  | /api/payment        | 500 | 0    | Server Overload
28. [2026-02-12 10:00:19] | 66.77.88.101  | GET  | /api/payment        | 500 | 0    | Server Overload
29. [2026-02-12 10:00:20] | 66.77.88.102  | GET  | /api/payment        | 500 | 0    | Server Overload
30. [2026-02-12 10:00:20] | 66.77.88.103  | GET  | /api/payment        | 500 | 0    | Server Overload

31. [2026-02-12 10:00:21] | 89.23.11.10   | GET  | /                   | 200 | 2048 | Normal Request
32. [2026-02-12 10:00:22] | 89.23.11.11   | GET  | /about              | 200 | 1024 | Normal Request
33. [2026-02-12 10:00:23] | 89.23.11.12   | GET  | /blog               | 200 | 2048 | Normal Request
34. [2026-02-12 10:00:24] | 89.23.11.13   | GET  | /services           | 200 | 2048 | Normal Request
35. [2026-02-12 10:00:25] | 89.23.11.14   | GET  | /pricing            | 200 | 1024 | Normal Request

36. [2026-02-12 10:00:26] | 144.91.22.1   | GET  | /api/auth           | 503 | 0    | Flood Pattern
37. [2026-02-12 10:00:26] | 144.91.22.2   | GET  | /api/auth           | 503 | 0    | Flood Pattern
38. [2026-02-12 10:00:27] | 144.91.22.3   | GET  | /api/auth           | 503 | 0    | Flood Pattern
39. [2026-02-12 10:00:27] | 144.91.22.4   | GET  | /api/auth           | 503 | 0    | Flood Pattern
40. [2026-02-12 10:00:28] | 144.91.22.5   | GET  | /api/auth           | 503 | 0    | Flood Pattern

41. [2026-02-12 10:00:29] | 51.210.45.60  | POST | /checkout           | 502 | 0    | Backend Timeout
42. [2026-02-12 10:00:30] | 51.210.45.61  | POST | /checkout           | 502 | 0    | Backend Timeout
43. [2026-02-12 10:00:30] | 51.210.45.62  | POST | /checkout           | 502 | 0    | Backend Timeout
44. [2026-02-12 10:00:31] | 51.210.45.63  | POST | /checkout           | 502 | 0    | Backend Timeout
45. [2026-02-12 10:00:31] | 51.210.45.64  | POST | /checkout           | 502 | 0    | Backend Timeout

46. [2026-02-12 10:00:32] | 103.21.244.1  | GET  | /api/auth           | 503 | 0    | Botnet Traffic
47. [2026-02-12 10:00:33] | 103.21.244.2  | GET  | /api/auth           | 503 | 0    | Botnet Traffic
48. [2026-02-12 10:00:33] | 103.21.244.3  | GET  | /api/auth           | 503 | 0    | Botnet Traffic
49. [2026-02-12 10:00:34] | 103.21.244.4  | GET  | /api/auth           | 503 | 0    | Botnet Traffic
50. [2026-02-12 10:00:34] | 103.21.244.5  | GET  | /api/auth           | 503 | 0    | Botnet Traffic

"""