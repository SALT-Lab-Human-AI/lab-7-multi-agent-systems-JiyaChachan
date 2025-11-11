"""
Shared Configuration Module for AutoGen and CrewAI Lab Demo

This module provides a unified configuration interface for both AutoGen and CrewAI frameworks.
It loads environment variables from the root .env file and provides validation and configuration objects.

Usage:
    from shared_config import Config

    # Validate configuration
    if not Config.validate():
        exit(1)

    # Use configuration
    api_key = Config.OPENAI_API_KEY
    config_list = Config.get_config_list()  # For AutoGen
"""

import os
from pathlib import Path
from typing import Dict, List, Any
from dotenv import load_dotenv


class Config:
    """
    Unified configuration class for both AutoGen and CrewAI

    Loads environment variables from the root .env file and provides access to shared settings.
    """

    # Load environment variables from root .env file
    _env_path = Path(__file__).parent / ".env"
    load_dotenv(_env_path)

    # ====================
    # OpenAI API Settings
    # ====================
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    OPENAI_API_BASE = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview")

    # ====================
    # Agent Settings
    # ====================
    AGENT_TEMPERATURE = float(os.getenv("AGENT_TEMPERATURE", "0.7"))
    AGENT_MAX_TOKENS = int(os.getenv("AGENT_MAX_TOKENS", "2000"))
    AGENT_TIMEOUT = int(os.getenv("AGENT_TIMEOUT", "300"))

    # ====================
    # Logging Settings
    # ====================
    VERBOSE = os.getenv("VERBOSE", "True").lower() == "true"
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"

    # ====================
    # Project Paths
    # ====================
    PROJECT_ROOT = Path(__file__).parent
    AUTOGEN_DIR = PROJECT_ROOT / "autogen"
    CREWAI_DIR = PROJECT_ROOT / "crewai"

    @classmethod
    def validate(cls) -> bool:
        """
        Validate that all required configurations are set.

        Returns:
            bool: True if configuration is valid, False otherwise
        """
        if not cls.OPENAI_API_KEY or cls.OPENAI_API_KEY == "":
            print("❌ ERROR: OPENAI_API_KEY is not configured!")
            print("\n📋 To fix this:")
            print("   1. Copy the .env.example file to .env:")
            print("      cp .env.example .env")
            print("   2. Add your OpenAI API key to the .env file")
            print("   3. Save the file")
            return False

        if not cls.OPENAI_API_BASE:
            print("⚠️  WARNING: OPENAI_API_BASE is not configured, using default")

        if not cls.OPENAI_MODEL:
            print("⚠️  WARNING: OPENAI_MODEL is not configured, using default")

        return True

    @classmethod
    def get_config_list(cls) -> List[Dict[str, Any]]:
        """
        Get configuration list formatted for AutoGen.

        Returns:
            List[Dict[str, Any]]: Configuration list for AutoGen agent initialization

        Example:
            config_list = Config.get_config_list()
            # Use with AutoGen:
            assistant = autogen.AssistantAgent(
                name="assistant",
                llm_config={"config_list": config_list}
            )
        """
        return [
            {
                "model": cls.OPENAI_MODEL,
                "api_key": cls.OPENAI_API_KEY,
                "api_base": cls.OPENAI_API_BASE,
                "api_type": "openai",
                "temperature": cls.AGENT_TEMPERATURE,
                "max_tokens": cls.AGENT_MAX_TOKENS,
                "timeout": cls.AGENT_TIMEOUT,
            }
        ]

    @classmethod
    def to_dict(cls) -> Dict[str, Any]:
        """
        Export all configuration as a dictionary.

        Returns:
            Dict[str, Any]: Dictionary containing all configuration values
        """
        return {
            "openai_api_key": cls.OPENAI_API_KEY,
            "openai_api_base": cls.OPENAI_API_BASE,
            "openai_model": cls.OPENAI_MODEL,
            "agent_temperature": cls.AGENT_TEMPERATURE,
            "agent_max_tokens": cls.AGENT_MAX_TOKENS,
            "agent_timeout": cls.AGENT_TIMEOUT,
            "verbose": cls.VERBOSE,
            "debug": cls.DEBUG,
        }

    @classmethod
    def print_summary(cls) -> None:
        """
        Print a summary of the current configuration (without exposing API key).
        """
        print("\n" + "="*60)
        print("📋 Configuration Summary")
        print("="*60)
        api_key_masked = (
            cls.OPENAI_API_KEY[:7] + "***" + cls.OPENAI_API_KEY[-4:]
            if cls.OPENAI_API_KEY and len(cls.OPENAI_API_KEY) > 11
            else "NOT SET"
        )
        print(f"✓ OpenAI API Key:    {api_key_masked}")
        print(f"✓ API Base:          {cls.OPENAI_API_BASE}")
        print(f"✓ Model:             {cls.OPENAI_MODEL}")
        print(f"✓ Temperature:       {cls.AGENT_TEMPERATURE}")
        print(f"✓ Max Tokens:        {cls.AGENT_MAX_TOKENS}")
        print(f"✓ Timeout:           {cls.AGENT_TIMEOUT}s")
        print(f"✓ Verbose:           {cls.VERBOSE}")
        print(f"✓ Debug:             {cls.DEBUG}")
        print("="*60 + "\n")


# Convenience functions for quick access
def validate_config() -> bool:
    """Quick function to validate configuration."""
    return Config.validate()


def get_openai_config() -> Dict[str, Any]:
    """Quick function to get OpenAI configuration."""
    return {
        "api_key": Config.OPENAI_API_KEY,
        "api_base": Config.OPENAI_API_BASE,
        "model": Config.OPENAI_MODEL,
    }


def get_agent_config() -> Dict[str, Any]:
    """Quick function to get agent configuration."""
    return {
        "temperature": Config.AGENT_TEMPERATURE,
        "max_tokens": Config.AGENT_MAX_TOKENS,
        "timeout": Config.AGENT_TIMEOUT,
    }


if __name__ == "__main__":
    """
    Test the configuration module.
    Run this file to verify that configuration is properly loaded:
        python shared_config.py
    """
    print("🧪 Testing Shared Configuration Module")
    print("-" * 60)

    if Config.validate():
        print("✅ Configuration validation passed!\n")
        Config.print_summary()
    else:
        print("❌ Configuration validation failed!")
        exit(1)
