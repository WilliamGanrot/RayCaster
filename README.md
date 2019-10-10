# RayCaster

A simple ray caster created in python3 and pygame. Using a matrix to generate a 2d map. A particle can move around inside the map and cast rays in its field of view. Uses line-to-line intersection to detect if a ray intersects with a wall. It uses an algorithm to minimize the amount of walls to optimize performence. Instead of creating four new walls for each tile it check if a wall is even needed or if it can extend an allready existing wall before creating a new one. With help of the length of the intersecting rays length we can generate a 3d environment.

![Image](exampleImg.png?raw=true "Title")

The program isn't in anyway perfect or completly bug free, the project was only created to try out raycasting
