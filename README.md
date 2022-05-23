# stc-kliwongan-2022
Shopify Technical Challenge Submission for the Backend Developer Intern position

## Tech stack:
- FastAPI
- SQLAlchemy
- React JS + Bootstrap

## Additional tech stack (not reflected on the repo)
- Heroku (backend since Replit cannot run two terminals for the frontend AND backend)
- CORS proxy server using CORS anywhere(to allow Replit to query the API since Heroku's CORS config is complicated)

## Instructions

The app itself is mostly self explanatory. The navigation bar and the buttons/links on each item explain their purposes too.
I will only explain very specific details.

### Item refreshing

If items or updates do not refresh after CRUD and undelete operations, please refresh the page.

### Creating items

Since I am not running form validation, even if you do submit empty fields, an item will be created regardless.

### Updating items

Since the values have placeholders, you only have to fill in the inputs that you want to change.
If you leave the rest blank, the values will stay the same.

## Additional notes

NOTE: If the navbar does not toggle, please expand your screen size so you can access the navbar items.

NOTE: If you're curious, we have a Swagger UI running on
https://stc-kliwn-backend.herokuapp.com/docs where you can play around with the web requests yourselves!
