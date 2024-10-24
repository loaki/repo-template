import pkgutil
from types import ModuleType
from typing import (
    Any,
    Dict,
)


def extract__all__from_submodules(module: ModuleType) -> Dict[str, Any]:
    """
    Walk all submodules in the module and collect all the variables exposed through `__all__`
    """
    all_settings: Dict[str, Dict[str, Any]] = {}
    for module_info in pkgutil.walk_packages(module.__path__):
        module_name = module_info.name
        full_module_name = f"{module.__package__}.{module_name}"
        all_settings[module_name] = {}
        module_spec = module_info.module_finder.find_spec(full_module_name)  # type: ignore
        if not module_spec or not module_spec.loader:
            continue
        submodule = module_spec.loader.load_module(full_module_name)
        if not hasattr(submodule, "__dict__") or not hasattr(submodule, "__all__"):
            continue
        module_all = {name: submodule.__dict__[name] for name in submodule.__all__}
        all_settings[module_name] = module_all
    return all_settings
