"""
BOOTCAMPERS DO NOT MODIFY THIS FILE.

Test drone state simulation with a figure 8.
"""

from modules import commands
from modules import drone_status
from modules import location
from modules.private.simulation.drone import drone_state


TIME_STEP_SIZE = 0.01  # seconds


def figure8() -> int:
    """
    main.
    """
    initial_position = location.Location(0.0, 0.0)
    boundary_top_left = location.Location(-11.0, -11.0)
    boundary_bottom_right = location.Location(11.0, 11.0)
    result, drone = drone_state.DroneState.create(
        TIME_STEP_SIZE,
        initial_position,
        boundary_top_left,
        boundary_bottom_right,
    )
    if not result:
        return -1

    # Get Pylance to stop complaining
    assert drone is not None

    # 0: Top right corner
    # 1: Bottom right corner
    # 2: Centre
    # 3: Bottom left corner
    # 4: Top left corner
    # 5: Centre
    # 6: Left
    # 7: Centre
    waypoint_index = 0
    waypoints = [
        commands.Command.create_set_relative_destination_command( 3.0,  4.0),
        commands.Command.create_set_relative_destination_command( 0.0, -8.0),
        commands.Command.create_set_relative_destination_command(-3.0,  4.0),
        commands.Command.create_set_relative_destination_command(-3.0, -4.0),
        commands.Command.create_set_relative_destination_command( 0.0,  8.0),
        commands.Command.create_set_relative_destination_command( 3.0, -4.0),
        commands.Command.create_set_relative_destination_command(-3.0,  0.0),
        commands.Command.create_set_relative_destination_command( 3.0,  0.0),
        commands.Command.create_land_command(),
    ]

    report, step = drone.run(commands.Command.create_null_command())
    while report.status != drone_status.DroneStatus.LANDED and step < 1000:
        command = commands.Command.create_null_command()
        if report.status == drone_status.DroneStatus.HALTED:
            print(step)
            print(waypoint_index)
            location_x = report.position.location_x
            location_y = report.position.location_y
            print("Halt: " + str(location_x) + ", " + str(location_y))
            command = waypoints[waypoint_index]
            waypoint_index += 1

        report, step = drone.run(command)

    print("At: " + str(report.position.location_x) + ", " + str(report.position.location_y))
    print("Steps: " + str(step))

    if report.status != drone_status.DroneStatus.LANDED:
        return -2

    return 0


if __name__ == "__main__":
    # Not a constant
    # pylint: disable-next=invalid-name
    status = figure8()
    if status < 0:
        print("ERROR: Status code: " + str(status))

    print("Done!")
