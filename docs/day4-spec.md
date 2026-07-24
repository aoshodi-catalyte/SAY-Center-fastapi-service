What are the exact endpoints (method + path) that satisfy the business requirements above?
What does the request body look like for each, if any?
What does a successful response look like for each — status code and body shape?
What does a failure response look like for requirement 4 — status code and body shape?
Where does validation happen, and where does "talking to the database" happen? (You've now seen Pydantic schemas, SQLAlchemy models, and route functions — how do those three responsibilities get divided?)
What decision did you make about which fields come back in a response, and why?
