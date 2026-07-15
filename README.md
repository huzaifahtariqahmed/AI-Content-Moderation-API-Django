# Build an AI Content Moderation API

---

![Image](https://nextwork.ai/courageous_orange_swift_hare/uploads/c07fb476-bd7b-4f0e-a59c-319aa9a3a6d7_tvbmghb1)

## Project Vision: Building a Production-Grade AI Moderation API

### Why this project matters

I'm building because it teaches me Django + DRF and allows me to build using these frameworks. It exposes me to AI endpoints, and how we wire up a production AI system.

## Setting Up the Django Project with DRF and Authentication

### Project setup goals

In this step, I'm setting up my project directory, installing dependancies, setting up a virtual environment, and doing scafolding so that I can start working on the actual API, with a proper structure.

![Image](https://nextwork.ai/courageous_orange_swift_hare/uploads/c07fb476-bd7b-4f0e-a59c-319aa9a3a6d7_82bpbn9y)

### Packages installed and REST_FRAMEWORK configuration

I installed django, anthropic sdk, django rest framework, python-dotenv, django filter

The REST_FRAMEWORK dict configures rules for APIs like authentication, permission, pagination, filterting.

## Designing the Data Model and Serializer Layer

### Model and serializer design goals

In this step, I'm designing model and serializers for the api so that the API can process input and send structured output, while the model defines what gets stored in the db.

![Image](https://nextwork.ai/courageous_orange_swift_hare/uploads/c07fb476-bd7b-4f0e-a59c-319aa9a3a6d7_3o575c58)

### Separating input and output serializers

The input serializer handles the input contnet send with api request bu the user, handling validation of the content sent, while the output serializer structurees the response of the api.

## Integrating Claude AI as a Content Moderation Service

### Service layer architecture

In this step, I'm building a service module to serve user content to AI endpoints and receive the response so that my API can parse it and structure it in a proper format.

### Live AI moderation results from the Django shell

I called moderate_content with the text "I love puppies" and the result showed {'category': 'safe', 'severity_score': 0.0, 'reasoning': 'Innocent statement expressing affection for puppies. No harmful, offensive, or inappropriate content.'}

## Wiring Up Authenticated API Endpoints with ViewSets

### ViewSet and URL configuration goals

In this step, I'm setting up my Viewsets and URLs so that I can send my moderation text to the Ai service layer via http request, and get a structured output back.

### User-scoped queryset and multi-user security

The get_queryset method filters the db records based on the user who has sent the request. This matters because it prevents a security threat where any user could potentially get moderation data for any other user.

## Validating Filtering, Pagination, and User Isolation

### End-to-end testing strategy

In this step, I'm testing the created api so that I can confirm the api works for multiple users, handles filtering as well as pagination, and respects user permissions.

![Image](https://nextwork.ai/courageous_orange_swift_hare/uploads/c07fb476-bd7b-4f0e-a59c-319aa9a3a6d7_hloe4d4h)

### Confirming per-user data isolation

I confirmed user isolation by creating a second user, submitting content as that user, and then sending a fetch moderion request as the first user to see if this request created by the second user is showing in the response or not. It was not meaning isolation is working.

## Extending the API with a Bulk Moderation Endpoint

### Custom bulk action with @action decorator

In this project extension, I added a bulk action that structures the data and using ModerationSubmitSerializer, and then in aloop we call the AI service layer (moderate_content) method for each child in the bulk content list submitted by the user, within the loop after we get back the response from AI, we create entry for that child in db and then append the db record we created to a list which then our output serializer (ModerationRequestSerializer) strucutres into a proper response format.

The response is a list of these moderation responses we were getting for are original post api.

## Reflections and Key Takeaways

### Tools and concepts mastered

The key tools I used include django, django rest framework, anthropic sdk. Key concepts I learnt include Django Project Scafolding, Models and Serializers, AI Service Layer, Viewsets and URLs, Testing, Decorators (Custom Bulk APIs), and much more. 

### Time and challenges

This project took me approximately 7-8 hours in a span of 1.5 weeks. The most challenging part was Viewsets understanding for me, as django removes so much of the abstraction that it becomes difficult to understand what Django handles on its own and what we have to handle.

### Looking ahead

I did this project today to learn how to work with Django and DRF to build and understand APIs, apps, shell, serializers, models, views and viewsets, service architecture, and much more. Another skill I want to learn is Fast API, and integration with Langchain and RAG systems.

---

*Built by [Huzaifah Tariq Ahmed](https://github.com/huzaifahtariqahmed)
