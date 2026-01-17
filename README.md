# Vestel ECV04 Wallbox Integration

This is a Home Assistant custom integration for the Vestel ECV04 Wallbox.

## Installation

### Via HACS (Custom Repository)

Since this integration is not yet available in the default HACS store, you can add it as a custom repository:

1. Ensure you have [HACS](https://hacs.xyz/) installed in Home Assistant.
2. In HACS, click the three dots (⋮) in the top-right corner and select **Custom repositories**.
3. Add the repository URL: `https://github.com/dominikandreas/vestel_ecv04_ha_integration`
4. Select **Integration** as the category.
5. Click **Add**.
6. Go to the Integrations tab in HACS, search for "Vestel ECV04 Wallbox", and install it.
7. Restart Home Assistant.
8. Add the integration via the UI: Settings > Devices & Services > Add Integration > Vestel ECV04 Wallbox.

### Manual Installation

1. Download the latest release from [GitHub](https://github.com/dominikandreas/vestel_ecv04_ha_integration/releases).
2. Extract the `custom_components/vestel_ecv04` folder to your Home Assistant's `custom_components` directory.
3. Restart Home Assistant.
4. Add the integration via the UI.

## Configuration

After installation, configure the integration by providing the IP address of your Vestel ECV04 Wallbox.

## Features

- Monitor charging status
- Control charging
- Sensor data

## Support

For issues, please create an issue on [GitHub](https://github.com/dominikandreas/vestel_ecv04_ha_integration/issues).

## License

MIT