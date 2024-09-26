# FitTrack Telegram Bot

## Configuration

We use [Pydantic Settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings) for project configuration
management. The entire configuration model is defined in `bot/config.py`. If you are new to this library, we recommend
reading the [Field Value Priority](https://docs.pydantic.dev/latest/concepts/pydantic_settings/#field-value-priority)
section to understand how the settings model populates configuration values.

All non-default configurations are placed in the `.env` file. A template for this file is available in `.env.example`.
If a value is specified in `.env.example` but not in `.env`, the value from `.env.example` will be used. This feature is
primarily utilized for Docker Compose settings, so you don't have to specify them manually in `.env` if you are using
Docker Compose.

If you are unsure where to get some configuration values, check 1Password for them. Additionally, if you update any
configurations, don't forget to update them in 1Password to keep everything synchronized.

Default values in the settings class should be suitable for the production environment, not development. Please keep
this in mind when adding new fields.
