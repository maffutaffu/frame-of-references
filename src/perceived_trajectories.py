from manim import *
#from src.objects.labeled_axes import *
#from src.objects.observer import *
from objects.observer import *
from objects.labeled_axes import *


class Introduction(Scene):
    def construct(self):
        # this is just a quick and lazy way of having centered text
        title = Text("Trajectories of")
        title2 = Text("Objects in Motion")
        group = VGroup(title, title2).arrange(DOWN).set_color_by_gradient(GREEN, ORANGE).scale(2)
        self.play(Write(group))
        self.wait(5)


# this one is gonna be fun
class DemonstrationOfPerceivedTrajectories(GraphScene):
    def __init__(self):
        GraphScene.__init__(
            self,
            y_min=-1,
            y_max=5,
            y_axis_label="$y$",
            x_min=-1,
            x_max=9,
            x_axis_label="$x$"
        )

    def construct(self):
        # drawing axes
        self.setup_axes(animate=True)
        self.wait()

        # adding stationary observer
        stationary_observer = Observer(colour=RED).move_to(self.coords_to_point(4, 5)).scale(0.8).rotate(PI)

        # adding time indication
        time_label = Tex("$t=$").move_to(self.coords_to_point(8, 5))
        time_number = DecimalNumber(0, num_decimal_places=3, include_sign=False, show_ellipsis=False) \
            .next_to(time_label, direction=RIGHT)

        # i'm sorry
        time_line = Line(ORIGIN, 4*RIGHT, stroke_opacity=0)
        time_dot = Dot(ORIGIN, stroke_opacity=0, fill_opacity=0)
        time_number.add_updater(lambda d: d.set_value(time_dot.get_x()))

        # adding car and moving to around the origin
        # Shift the car lower so the observer appears to be in the car.
        car = Rectangle(color=WHITE, height=0.5, width=1.5, fill_opacity=1, fill_color=WHITE) \
            .move_to(self.coords_to_point(-0.5, -0.25))

        # adding moving observer
        moving_observer = Observer(colour=BLUE).scale(0.4).rotate(-PI/2) \
            .move_to(self.coords_to_point(-0.75, 0))

        # adding projectile
        projectile = Circle(radius=0.25, color=GREEN, fill_opacity=1, fill_color=GREEN)
        projectile.move_to(self.coords_to_point(0, 0))

        # adding updater for car moving and moving observer
        # Strange that they follow the projectile...
        # Anyways, only update the X coordinate to make configuration much easier.
        car.add_updater(lambda d: d.set_x(projectile.get_x() - 0.25))
        moving_observer.add_updater(lambda d: d.set_x(car.get_x() - 0.25))

        # adding path for the object
        path = self.get_graph(self.trajectory, x_min=0, x_max=0, color=BLUE)
        path.add_updater(lambda d: d.become(
            self.get_graph(self.trajectory,
                           x_min=0,
                           # this is done so that the graph can seem to be traced out by the ball
                           x_max=self.point_to_coords(projectile.get_x())[0]).set_color(BLUE)))

        self.play(
            ShowCreation(stationary_observer),
            Write(time_label),
            Write(time_number),
            # path is added first to ensure that the projectile will always be on top when moving
            ShowCreation(path),
            ShowCreation(car),
            ShowCreation(moving_observer),
            ShowCreation(projectile),
            ShowCreation(time_dot),
            ShowCreation(time_line)
        )
        self.wait(7)
        self.play(
            MoveAlongPath(projectile, self.get_graph(self.trajectory, x_min=0, x_max=8)),
            MoveAlongPath(time_dot, time_line),
            rate_func=linear, run_time=4)
        self.wait()

    def trajectory(self, x):
        return -1/4*(x**2)+(2*x)


class StationaryPerspective(GraphScene):
    def __init__(self):
        GraphScene.__init__(
            self,
            y_min=-1,
            y_max=5,
            y_axis_label="$y$",
            x_min=-1,
            x_max=9,
            x_axis_label="$x$"
        )

    def construct(self):
        # drawing axes
        self.setup_axes(animate=True)
        self.wait()

        # adding stationary observer
        stationary_observer = Observer(colour=RED)
        stationary_observer.move_to(self.coords_to_point(4, 5)).scale(0.8).rotate(PI)

        # adding time indication
        time_label = Tex("$t=$")
        time_label.move_to(self.coords_to_point(8, 5))
        time_number = DecimalNumber(0, num_decimal_places=2, include_sign=False, show_ellipsis=False) \
            .next_to(time_label, direction=RIGHT)
        # i'm sorry, best thing I have for a time keeping thing
        time_line = Line(ORIGIN, 4 * RIGHT, stroke_opacity=0)
        time_dot = Dot(ORIGIN, stroke_opacity=0, fill_opacity=0)
        time_number.add_updater(lambda d: d.set_value(time_dot.get_x()))

        # adding projectile
        projectile = Circle(radius=0.25, color=GREEN, fill_opacity=1, fill_color=GREEN)
        projectile.move_to(self.coords_to_point(0, 0))

        # adding path for the object
        path = self.get_graph(self.trajectory, x_min=0, x_max=0, color=BLUE)
        path.add_updater(lambda d: d.become(
            self.get_graph(self.trajectory,
                           x_min=0,
                           # this is done so that the graph can seem to be traced out by the ball
                           x_max=self.point_to_coords(projectile.get_x())[0]).set_color(BLUE)))

        # adding velocity vectors
        # this code is even worse, ugh someone please tell me a better way to keep track of time!!!
        x_vector = Line(
            np.array([projectile.get_x(), projectile.get_y(), 0]),
            np.array([projectile.get_x()+2, projectile.get_y(), 0])
        ).add_tip().set_color(RED_A)

        x_vector.add_updater(lambda d: d.become(Line(
            np.array([projectile.get_x(), projectile.get_y(), 0]),
            np.array([projectile.get_x()+2, projectile.get_y(), 0])
        ).add_tip().set_color(RED_A)))

        y_vector = Line(
            np.array([projectile.get_x(), projectile.get_y(), 0]),
            np.array([projectile.get_x(), projectile.get_y()+(4-2*time_dot.get_x())/2, 0])  # see notes for calculations
        ).add_tip().set_color(BLUE_D)

        y_vector.add_updater(lambda d: d.become(Line(
            np.array([projectile.get_x(), projectile.get_y(), 0]),
            np.array([projectile.get_x(), projectile.get_y()+(4-2*time_dot.get_x())/2, 0])  # see notes for calculations
        ).add_tip().set_color(BLUE_D)))

        x_vector_label = Tex("$v_{x}=$")
        x_vector_value = DecimalNumber(2, num_decimal_places=2, show_ellipsis=False) \
            .next_to(x_vector_label, direction=RIGHT)

        x_label_group = VGroup(x_vector_label, x_vector_value).next_to(time_label, direction=DOWN)\
            .align_to(time_label, direction=LEFT).set_color(RED_A).shift(np.array([0, -0.2, 0]))

        y_vector_label = Tex("$v_{y}=$")
        y_vector_value = DecimalNumber(4, num_decimal_places=2, show_ellipsis=False) \
            .next_to(y_vector_label, direction=RIGHT)

        y_label_group = VGroup(y_vector_value, y_vector_label).next_to(x_label_group, direction=DOWN) \
            .align_to(time_label, direction=LEFT).set_color(BLUE_D).shift(np.array([0, -0.2, 0]))

        y_vector_value.add_updater(lambda d: d.set_value(4-2*time_dot.get_x()))

        self.play(
            ShowCreation(stationary_observer),
            Write(time_label),
            Write(time_number),
            # path is added first to ensure that the projectile will always be on top when moving
            ShowCreation(path),
            ShowCreation(time_dot),
            ShowCreation(time_line),
            ShowCreation(x_vector),
            # ShowCreation(x_vector_label),
            # ShowCreation(x_vector_value),
            ShowCreation(y_vector),
            FadeIn(projectile),
            # ShowCreation(y_vector_label),
            # ShowCreation(y_vector_value)
            ShowCreation(y_label_group),
            ShowCreation(x_label_group)
        )
        self.wait()
        self.play(
            MoveAlongPath(projectile, self.get_graph(self.trajectory, x_min=0, x_max=8)),
            MoveAlongPath(time_dot, time_line),
            rate_func=linear, run_time=4)
        self.wait(7)

    def trajectory(self, x):
        return -1 / 4 * (x ** 2) + (2 * x)


class MovingReferenceFrame(GraphScene, MovingCameraScene):
    def __init__(self):
        GraphScene.__init__(
            self,
            y_min=-1,
            y_max=6,
            y_axis_label="$y$",
            x_min=-1,
            x_max=9,
            x_axis_label="$x$"
        )

    def setup(self):
        GraphScene.setup(self)
        MovingCameraScene.setup(self)

    def construct(self):
        self.setup_axes(animate=True)
        self.wait()

        self.camera_frame.save_state()

        # TODO: consider removing this.
        scaling = Text("the y axis is scaled for illustrative purposes")
        scaling.move_to(3*UP).scale(0.5)

        self.play(Write(scaling), run_time=0.5)
        moving_observer = Observer(colour=BLUE).scale(0.4).rotate(-PI / 2)

        # adding time indication
        time_label = Tex("$t=$")
        time_label.next_to(moving_observer, direction=DOWN)
        time_number = DecimalNumber(0, num_decimal_places=3, include_sign=False, show_ellipsis=False)
        time_number.next_to(time_label, direction=RIGHT)
        time_number.add_updater(lambda d: d.next_to(time_label, direction=RIGHT))
        # i'm sorry
        time_line = Line(ORIGIN, 4 * RIGHT, stroke_opacity=0)
        time_dot = Dot(ORIGIN, stroke_opacity=0, fill_opacity=0)
        time_number.add_updater(lambda d: d.set_value(time_dot.get_x()))
        time_label.add_updater(lambda d: d.next_to(moving_observer, direction=DOWN))
        # adding projectile
        projectile = Circle(radius=0.25, color=GREEN, fill_opacity=1, fill_color=GREEN) \
            .move_to(self.coords_to_point(0, 0))

        # adding vectors
        y_vector = Line(
            np.array([projectile.get_x(), projectile.get_y(), 0]),
            np.array([projectile.get_x(), projectile.get_y() + (4 - 2 * time_dot.get_x()) / 4, 0])
            # see notes for calculations
        ).add_tip().set_color(BLUE_A)

        y_vector.add_updater(lambda d: d.become(Line(
            np.array([projectile.get_x(), projectile.get_y(), 0]),
            np.array([projectile.get_x(), projectile.get_y() + (4 - 2 * time_dot.get_x()) / 4, 0])
            # see notes for calculations
        ).add_tip().set_color(BLUE_A)))

        moving_observer.next_to(projectile, direction=LEFT)
        moving_observer.add_updater(lambda d: d.move_to(
            np.array([projectile.get_x()-0.5, -2.5, 0])))

        # adding path
        path = self.get_graph(self.trajectory, x_min=0, x_max=0, color=BLUE)
        path.add_updater(lambda d: d.become(
            self.get_graph(self.trajectory,
                           x_min=0,
                           # this is done so that the graph can seem to be traced out by the ball
                           x_max=self.point_to_coords(projectile.get_x())[0]).set_color(BLUE)))
        self.play(Write(time_label),
                  ShowCreation(time_dot),
                  ShowCreation(time_number),
                  ShowCreation(moving_observer),
                  ShowCreation(path),
                  ShowCreation(y_vector),
                  FadeIn(projectile),
                  )

        # Apparently the updater won't be called unless you animate the object.
        self.play(self.camera_frame.animate.move_to(
            np.array([moving_observer.get_x(), moving_observer.get_y(), 0]))
            # Move the camera up a bit so it does not cover useless space.
            .shift(UP * 2).scale(0.75))

        def update_camera(camera):
            camera.move_to(np.array([moving_observer.get_x(), moving_observer.get_y() + 2, 0]))

        self.camera_frame.add_updater(update_camera)
        self.wait(6)
        self.play(MoveAlongPath(projectile, self.get_graph(self.trajectory, x_min=0, x_max=8)),
                  MoveAlongPath(time_dot, time_line),
                  rate_func=linear, run_time=4)
        self.camera_frame.remove_updater(update_camera)
        self.play(Restore(self.camera_frame))

        self.wait()

    def trajectory(self, x):
        return -1 / 4 * (x ** 2) + (2 * x)


class WhichReferenceFrame(Scene):
    def construct(self):
        moving_observer = Observer(colour=BLUE).move_to(LEFT)
        stationary_observer = Observer(colour=RED).move_to(RIGHT)

        words = [
            Text("or"),
            Text("?")
        ]


        words[1].next_to(stationary_observer, direction=RIGHT)
        words_group = VGroup(words[0], words[1])
        observers = VGroup(moving_observer, stationary_observer)
        self.play(ShowCreation(observers), Write(words_group))
        self.wait()
        self.clear()

        relative = MarkupText('Motion is <color col="GREEN">relative</color>')
        self.play(Write(relative))
        self.wait(3)




