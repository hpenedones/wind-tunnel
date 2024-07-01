"""Example run of a WindTunnel scenario based on Inductiva API."""

from absl import app, flags, logging

import windtunnel

FLAGS = flags.FLAGS
flags.DEFINE_boolean('debug', False, 'Enable debug mode')
flags.DEFINE_boolean('display', False,
                     'Open PyVista window with inputs visualization')
flags.DEFINE_string('object_path', 'assets/f1_car.obj',
                    'Path to the object file')
flags.DEFINE_string(
    'machine_group_name', None,
    'Machine group to run the simulation on. Defaults to default queue')


def main(_):

    if FLAGS.debug:
        logging.set_verbosity(logging.DEBUG)

    # Initialize the scenario
    wind_tunnel = windtunnel.WindTunnel()

    # Submit the simulation task
    task = wind_tunnel.simulate(object_path=FLAGS.object_path,
                                wind_speed_ms=10,
                                rotate_z_degrees=0,
                                num_iterations=50,
                                resolution=3,
                                display=FLAGS.display,
                                machine_group_name=FLAGS.machine_group_name)

    print(f'To visualize results, run:\n\n'
          f'python view_outputs.py --task_id {task.id}\n')


if __name__ == '__main__':
    logging.set_verbosity(logging.INFO)
    app.run(main)
