import logging
import os
import httpx2
from mcp.server import MCPServer
from pathlib import Path
from dotenv import load_dotenv

# Load .env from the same directory as weather.py
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(env_path)

logging.basicConfig(level=logging.INFO)

WEATHER_KEY = os.getenv("WEATHER_API_KEY")

# Create MCP Server
mcp = MCPServer(name="Weather Checker",version="1.0.0")

#create tool
@mcp.tool()
async def weather_checker(city: str) -> str:
    """
    Fetch live weather data for any city using the weather API.

    Call this tool whenever the user asks about current weather
    in a location, including questions such as:
    - What is the weather in Noida?
    - What is the temperature in Delhi?
    - Is it raining in Mumbai?

    Args:
        city: The city requested by the user, e.g. Noida or Delhi or New York
    """
    url = f"https://api.weatherapi.com/v1/current.json?key={WEATHER_KEY}&q={city}&aqi=yes"
    async with httpx2.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=30.0)
            data = response.json()
            return (
                    f"City:{city}\n"
                    f"Weather data:{data}"
                )
        except httpx2.HTTPError as e:
            return f"API error:{e}"


#run server
if __name__ == "__main__":
    if not WEATHER_KEY:
        logging.info("API key issue")
    logging.info("✅ MCP server: Weather Checker started")
    mcp.run(transport="stdio")