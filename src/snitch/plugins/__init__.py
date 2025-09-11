"""Handles loading and managing Snitch plugins."""

from importlib.metadata import EntryPoint, entry_points

from snitch.logging import logger


def _load_plugin(plugin_entry: EntryPoint):
    """Load a single plugin entry point."""
    try:
        plugin_class = plugin_entry.load()
        plugin_instance = plugin_class()

        if hasattr(plugin_instance, "is_applicable") and callable(plugin_instance.is_applicable):
            if plugin_instance.is_applicable():
                return plugin_instance
            else:
                logger.info(
                    f"Skipping plugin '{plugin_instance.name}' as it is not applicable to this system."
                )
        else:
            logger.warning(
                f"Skipping plugin '{plugin_entry.name}' because it does not have an 'is_applicable' method."
            )

    except ImportError as e:
        logger.warning(f"Could not load plugin '{plugin_entry.name}': {e}")

    return None


def load_plugins():
    """Discover, load, and filter all installed snitch plugins."""
    discovered_plugins = entry_points(group="snitch.plugins")
    if not discovered_plugins:
        logger.warning("No plugins discovered for group 'snitch.plugins'")
        return []

    applicable_plugins = []
    for plugin_entry in discovered_plugins:
        plugin = _load_plugin(plugin_entry)
        if plugin:
            applicable_plugins.append(plugin)

    logger.info(f"Applicable plugins: {[p.name for p in applicable_plugins]}")
    return applicable_plugins
