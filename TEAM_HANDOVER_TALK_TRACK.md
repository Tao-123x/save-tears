# Save Tears Handover Talk Track

This file is a speaking guide for the English team handover deck.  
Use it to rehearse the presentation in a natural order.

## Opening

Today I will give a handover of my current project, Save Tears.  
The goal is to show what is already working, what is still incomplete, how the codebase is organized, and how we can split the next phase of work as a team.

## Slide 1 - Project Overview

Save Tears is a water conservation management system.  
It has a uni-app mini-program frontend and a FastAPI backend.  
At the moment, the most complete part is the end-to-end flow for registration, login, and room-based lookup of three data types.

## Slide 2 - Purpose Of This Meeting

This is not a final defense presentation.  
It is a handover and onboarding session for the team.  
I want everyone to leave with a clear idea of what is stable, what is still a prototype, and where to start in the codebase.

## Slide 3 - System Architecture

The structure is simple.  
The mini-program pages trigger user interactions.  
Those pages call the shared API wrapper in `src/api/index.ts`.  
The API wrapper sends HTTP requests to the FastAPI backend.  
The backend reads and writes through SQLAlchemy and returns JSON data to the frontend.  
The database is SQLite by default, with optional MySQL support through an environment variable.

## Slide 4 - What Is Already Working

The key working flow is: register, log in, store the user locally, and use the room number from that user object to query water flow, sewage turbidity, and water bill data.  
This part is real backend-connected functionality rather than just interface design.

## Slide 5 - Frontend Status By Page

I divide the frontend into three groups.  
First, the working business pages: login, register, water-flow, sewage-turbidity, and water-bill.  
Second, the partially dynamic pages: home and profile. They can read the logged-in username, but most of the content is still static or placeholder content.  
Third, the admin page, which is currently a UI prototype using mock data.

## Slide 6 - Backend APIs And Shared Interfaces

The main routes currently used by the mini-program are register, login, and the three GET routes for room-based lookup.  
There are also POST routes for submitting data and a route for reading users, but these are not connected to frontend pages yet.  
So the API groundwork is ahead of the UI in some places.

## Slide 7 - How To Read The Codebase Quickly

If you are new to the project, start with three files.  
First, `pages.json` to understand the page structure and navigation.  
Second, `src/api/index.ts` to understand request flow and available API functions.  
Third, `save_tears_backend/api.py` to understand models, schemas, routes, and database logic.  
Those three files give the quickest complete overview.

## Slide 8 - Current Gaps And Risks

I want to be explicit here.  
The home page is mostly static content.  
The profile page has several buttons that are not connected.  
The admin page uses mock data.  
The registration page has an email field in the UI, but the backend does not store email yet.  
Authentication is based on local storage, not tokens, and password handling is still plaintext.  
So the project is functional for development and demo purposes, but not production-ready.

## Slide 9 - Recommended Team Split

I suggest splitting the work by module.  
One area is frontend completion: home, profile, admin, and charts.  
One area is backend and security: email support, password hashing, auth cleanup, and API cleanup.  
One area is data input and visualization: building forms and connecting the existing submit APIs.  
One area is testing and integration: environment setup, sample data, regression checks, and documentation.

## Slide 10 - Live Demo Path

For the demo, I will keep the flow short and safe.  
I will register a user, log in, show the username on the home page, and open the three room-based data pages.  
Before the meeting, I need to make sure the backend is running, at least one room already has sample records, and local storage is clean.

## Slide 11 - Next Sprint Proposal

The next sprint can be split into three stages.  
Stage 1 is backend stabilization and basic security improvements.  
Stage 2 is converting placeholder pages into real features and connecting data input plus charts.  
Stage 3 is testing, polish, deployment, and presentation readiness.

## Closing

My main message is that the project already has a working core.  
The next step is not to restart it, but to make that core more complete, safer, and easier to maintain as a team project.

## Q And A Prep

If someone asks, "What is truly finished?"
Answer: registration, login, local user persistence, and room-based lookup for the three data pages.

If someone asks, "What is not finished yet?"
Answer: dynamic home content, real profile features, real admin workflows, proper auth, email persistence, and production-grade security.

If someone asks, "Where should I start in the codebase?"
Answer: start with `pages.json`, `src/api/index.ts`, and `save_tears_backend/api.py`.

If someone asks, "What can we do next as a team?"
Answer: split work by frontend completion, backend/security, data entry and charts, and testing/integration.
