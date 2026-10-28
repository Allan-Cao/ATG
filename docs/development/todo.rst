.. _active_development:

######
 Todo
######

*********
 Planned
*********

- Handle database sessions better than passing session objects around. I kind of like
  the current functional nature of the API
- Normalize database objects. Specifically the series/tournament-game relationship
- Reduce the number of nullable columns where possible. This is especially a problem on
  the game table
- Introduce enums where appropriate

***********
 Completed
***********

- Remove the usage of ``ratelimit`` in favor of something that actually does stable rate
  limiting
- Properly handle API error codes
- Add the ability to store draft / other available esports game information
- Open source GRID API code and GRID insertion scripts
- Transition to HTTPX > requests
- Add start/end dates to ``player_team_associations`` so team rosters can be tracked
  over time
