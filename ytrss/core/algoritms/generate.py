from ytrss.core.managers.manager_service import ManagerService, default_manager_service


async def generate(manager_service: ManagerService = default_manager_service()) -> None:
    """ Generate destination files. """
    for destination in manager_service.destination_manager.destinations:
        destination.on_finish(manager_service.templates_manager)
