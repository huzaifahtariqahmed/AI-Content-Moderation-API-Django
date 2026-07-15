# AI Content Moderation API

A Django REST Framework API that uses Claude (Anthropic) to classify submitted text as `safe`, `warning`, or `violation`, with per-user history, filtering, pagination, and a bulk submission endpoint.

---

## Tech Stack

- Python / Django 6.0
- Django REST Framework 3.17
- Anthropic SDK (Claude Haiku 4.5) for moderation
- Token authentication (`rest_framework.authtoken`)
- SQLite (default, dev)

## Setup

### 1. Clone and create a virtual environment

```bash
git clone https://github.com/huzaifahtariqahmed/AI-Content-Moderation-API-Django.git
cd AI-Content-Moderation-API-Django
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file in the project root:

```
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

### 4. Run migrations and create a superuser

```bash
python manage.py migrate
python manage.py createsuperuser
```

### 5. Start the dev server

```bash
python manage.py runserver
```

The API is now available at `http://127.0.0.1:8000/api/`.

## Authentication

The API uses DRF token authentication. Obtain a token with your username/password:

```bash
curl -X POST http://127.0.0.1:8000/api/token/ \
  -d "username=<your-username>&password=<your-password>"
```

Response:

```json
{ "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4" }
```

Include the token on every subsequent request:

```
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4
```

Every endpoint below requires this header. Results are scoped to the authenticated user — you will only ever see your own moderation requests.

## API Reference

Base path: `/api/moderations/`

### Submit content for moderation

```
POST /api/moderations/
```

Request body:

```json
{ "content": "I love puppies" }
```

`content` must be 1–5000 characters. The API calls Claude synchronously, stores the result, and returns it.

Response — `201 Created`:

```json
{
  "id": 1,
  "user": "huzaifah",
  "content": "I love puppies",
  "category": "safe",
  "severity_score": 0.0,
  "reasoning": "Innocent statement expressing affection for puppies. No harmful, offensive, or inappropriate content.",
  "created_at": "2026-07-16T12:00:00Z"
}
```

### Submit multiple items at once

```
POST /api/moderations/bulk/
```

Request body:

```json
{ "contents": ["first message", "second message"] }
```

`contents` accepts 1–10 items, each 1–5000 characters. Every item is moderated and stored individually.

Response — `201 Created`: a list of moderation objects in the same shape as the single-submit response.

### List your moderation history

```
GET /api/moderations/
```

Supports:
- **Filtering** — `?category=safe` (also `warning`, `violation`, `error`)
- **Ordering** — `?ordering=severity_score` or `?ordering=-created_at`
- **Pagination** — `?page=2` (10 results per page)

### Retrieve a single moderation record

```
GET /api/moderations/{id}/
```

Returns `404` if the record doesn't belong to the authenticated user.

## Moderation Categories

| Category    | Severity range | Meaning                                          |
|-------------|-----------------|--------------------------------------------------|
| `safe`      | 0.0 – 0.3       | Normal content, no issues                        |
| `warning`   | 0.3 – 0.7       | Borderline or mildly inappropriate                |
| `violation` | 0.7 – 1.0       | Clearly harmful, hateful, or dangerous            |
| `error`     | 0.0             | The moderation service failed to produce a result |

## Running Tests

```bash
python manage.py test
```

---

## Project Vision: Building a Production-Grade AI Moderation API

### Why this project matters

I'm building this because it teaches me Django + DRF and lets me build using these frameworks. It exposes me to AI endpoints and how to wire up a production AI system.

## Setting Up the Django Project with DRF and Authentication

### Project setup goals

In this step, I'm setting up my project directory, installing dependencies, setting up a virtual environment, and doing scaffolding so that I can start working on the actual API, with a proper structure.

![Image](https://nextwork.ai/courageous_orange_swift_hare/uploads/c07fb476-bd7b-4f0e-a59c-319aa9a3a6d7_82bpbn9y)

### Packages installed and REST_FRAMEWORK configuration

I installed Django, the Anthropic SDK, Django REST Framework, python-dotenv, and django-filter.

The REST_FRAMEWORK dict configures rules for APIs like authentication, permissions, pagination, and filtering.

## Designing the Data Model and Serializer Layer

### Model and serializer design goals

In this step, I'm designing the model and serializers for the API so that the API can process input and send structured output, while the model defines what gets stored in the DB.

![Image](https://nextwork.ai/courageous_orange_swift_hare/uploads/c07fb476-bd7b-4f0e-a59c-319aa9a3a6d7_3o575c58)

### Separating input and output serializers

The input serializer handles the content sent with the API request by the user, handling validation of the content sent, while the output serializer structures the response of the API.

## Integrating Claude AI as a Content Moderation Service

### Service layer architecture

In this step, I'm building a service module to send user content to AI endpoints and receive the response so that my API can parse it and structure it in a proper format.

### Live AI moderation results from the Django shell

I called `moderate_content` with the text "I love puppies" and the result showed `{'category': 'safe', 'severity_score': 0.0, 'reasoning': 'Innocent statement expressing affection for puppies. No harmful, offensive, or inappropriate content.'}`.

## Wiring Up Authenticated API Endpoints with ViewSets

### ViewSet and URL configuration goals

In this step, I'm setting up my ViewSets and URLs so that I can send my moderation text to the AI service layer via an HTTP request and get a structured output back.

### User-scoped queryset and multi-user security

The `get_queryset` method filters the DB records based on the user who sent the request. This matters because it prevents a security issue where any user could potentially get moderation data for any other user.

## Validating Filtering, Pagination, and User Isolation

### End-to-end testing strategy

In this step, I'm testing the created API so that I can confirm it works for multiple users, handles filtering and pagination, and respects user permissions.

![Image](https://nextwork.ai/courageous_orange_swift_hare/uploads/c07fb476-bd7b-4f0e-a59c-319aa9a3a6d7_hloe4d4h)

### Confirming per-user data isolation

I confirmed user isolation by creating a second user, submitting content as that user, and then sending a fetch-moderation request as the first user to see whether the request created by the second user showed up in the response. It did not, meaning isolation is working.

## Extending the API with a Bulk Moderation Endpoint

### Custom bulk action with @action decorator

In this project extension, I added a bulk action that validates the incoming list with `BulkModerationSubmitSerializer`, then loops over each item in the submitted content list, calling the AI service layer's `moderate_content` for each one. After each AI response comes back, a DB entry is created for that item and appended to a list, which the output serializer (`ModerationRequestSerializer`) then structures into a proper response format.

The response is a list of these moderation responses, matching the shape of the original single-submit endpoint.

## Reflections and Key Takeaways

### Tools and concepts mastered

The key tools I used include Django, Django REST Framework, and the Anthropic SDK. Key concepts I learned include Django project scaffolding, models and serializers, the AI service layer, ViewSets and URLs, testing, decorators (custom bulk APIs), and much more.

### Time and challenges

This project took me approximately 7–8 hours over a span of 1.5 weeks. The most challenging part was understanding ViewSets, since Django abstracts away so much that it becomes difficult to know what Django handles on its own versus what you have to handle yourself.

### Looking ahead

I did this project to learn how to work with Django and DRF to build and understand APIs, apps, the shell, serializers, models, views, ViewSets, and service architecture, among other things. Another skill I want to learn is FastAPI, along with integration with LangChain and RAG systems.

---

*Built by [Huzaifah Tariq Ahmed](https://github.com/huzaifahtariqahmed)*
