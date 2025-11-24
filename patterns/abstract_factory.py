from abc import ABC, abstractmethod


class Button(ABC):
    @abstractmethod
    def paint(self):
        pass


class WindowsButton(Button):
    def paint(self):
        print("Windows button")


class MacButton(Button):
    def paint(self):
        print("Mac button")


class Checkbox(ABC):
    @abstractmethod
    def paint(self):
        pass


class WindowsCheckbox(Checkbox):
    def paint(self):
        print("Windows checkbox")


class MacCheckbox(Checkbox):
    def paint(self):
        print("Mac checkbox")


class GUIFactory(ABC):
    @abstractmethod
    def create_button(self):
        pass

    @abstractmethod
    def create_checkbox(self):
        pass


class WindowsFactory(GUIFactory):
    def create_button(self):
        return WindowsButton()

    def create_checkbox(self):
        return WindowsCheckbox()


class MacFactory(GUIFactory):
    def create_button(self):
        return MacButton()

    def create_checkbox(self):
        return MacCheckbox()


class Application:
    def __init__(self, factory):
        self.button = factory.create_button()
        self.checkbox = factory.create_checkbox()

    def paint(self):
        self.button.paint()
        self.checkbox.paint()


if __name__ == "__main__":
    app_win = Application(WindowsFactory())
    app_mac = Application(MacFactory())
    app_win.paint()
    app_mac.paint()
