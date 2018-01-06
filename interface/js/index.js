"use strict";

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var CLICKED_ITEMS = [{
  component: "",
  feature: ""
}, {
  component: "",
  action: ""
}];

var LINKS = [{
  colorIndex: "graph-2",
  ids: ["light-switch", "light-off"],
  component: "light",
  feature: "switch"
}, {
  colorIndex: "graph-2",
  ids: ["arm-grip", "arm-stop"],
  component: "arm",
  feature: "grip"
}, {
  colorIndex: "graph-2",
  ids: ["arm-wrist", "arm-stop"],
  component: "arm",
  feature: "wrist"
}, {
  colorIndex: "graph-2",
  ids: ["arm-elbow", "arm-stop"],
  component: "arm",
  feature: "elbow"
}, {
  colorIndex: "graph-2",
  ids: ["arm-shoulder", "arm-stop"],
  component: "arm",
  feature: "shoulder"
}, {
  colorIndex: "graph-2",
  ids: ["base-direction", "base-stop"],
  component: "base",
  feature: "direction"
}];

var ROBOARM = {
  description: "OWI-535 Robotic Arm",
  identification: {
    description: "These are the parameters used to identify the RoboArm using the USB connection",
    idVendor: 0x1267,
    idProduct: 0x000
  },
  initialisation: {
    description: "These variables are used to transfer data on the created USB connection",
    bmRequestType: 0x40,
    bmRequest: 6,
    wValue: 0x100,
    wIndex: 0
  },
  components: {
    base: {
      description: "The <ARM> components are mounted on this rotating base, with approx. 270deg freedom, clockwise and counterclockwise rotation is considered from the top of the RoboArm",
      mask: 255,
      features: {
        direction: {
          mask: 3,
          actions: {
            ccw: 1,
            cw: 2,
            stop: 0
          }
        }
      }
    },
    arm: {
      description: "This component is mounted on the <BASE>, and replicates a typical human arm - with features, i.e. shoulder, elbow, wrist and a gripper.",
      mask: 255,
      features: {
        all: {
          description: "This is a pseudo-feature that allows for complex functions to be predescribed for the whole <ARM> component",
          mask: 255,
          type: "virtual",
          actions: {
            open: 170,
            close: 85,
            stop: 0
          }
        },
        shoulder: {
          description: "The first feature of the <ARM>, closest to the <BASE> offering 180deg of rotation, 0deg: parallel to <BASE>, 90deg: perpendicular",
          mask: 192,
          actions: {
            open: 64,
            close: 128,
            stop: 0
          }
        },
        elbow: {
          description: "",
          mask: 48,
          actions: {
            open: 16,
            close: 32,
            stop: 0
          }
        },
        wrist: {
          description: "",
          mask: 12,
          actions: {
            open: 4,
            close: 8,
            lift: 4,
            stop: 0
          }
        },
        grip: {
          description: "",
          mask: 3,
          actions: {
            open: 1,
            close: 2,
            grab: 2,
            drop: 1,
            stop: 0,
            pause: 0
          }
        }
      }
    },
    light: {
      description: "This is an LED mounted behind the <GRIP> feature on the <ARM> component - the focus of the light is useful to highlight where to grab, or that the system is in use",
      mask: 255,
      features: {
        switch: {
          description: "The only feature of the <LIGHT> is the <SWITCH>, simply flipping the last bit of the 3rd byte",
          mask: 1,
          actions: {
            on: 1,
            off: 0
          }
        }
      }
    }
  }
};

var RoboArmComponents = function (_React$Component) {
  _inherits(RoboArmComponents, _React$Component);

  function RoboArmComponents() {
    _classCallCheck(this, RoboArmComponents);

    return _possibleConstructorReturn(this, _React$Component.apply(this, arguments));
  }

  RoboArmComponents.prototype.render = function render() {
    var _this2 = this;

    var componentKeys = Object.keys(this.props.componentConfig);
    var componentParts = componentKeys.map(function (componentName) {
      return React.createElement(
        Topology.Part,
        {
          a11yTitle: componentName,
          className: "component",
          key: componentName,
          direction: "row"
        },
        React.createElement(RoboArmComponentFeatures, {
          featureConfig: _this2.props.componentConfig[componentName].features,
          componentName: componentName,
          onClick: _this2.props.onClick
        }),
        React.createElement(
          Topology.Label,
          { className: "raa_component_label" },
          componentName.toUpperCase()
        ),
        React.createElement(RoboArmControlFeatures, {
          featureConfig: _this2.props.componentConfig[componentName].features,
          controlName: componentName,
          onClick: _this2.props.onClick
        })
      );
    });
    return React.createElement(
      Topology.Part,
      {
        a11yTitle: "RoboArm Component Structure",
        className: "RoboArmComponents",
        direction: "column",
        label: this.props.roboArmName
      },
      React.createElement(
        Topology.Part,
        {
          a11yTitle: "RoboArm Component Structure",
          className: "RoboArmComponents",
          direction: "column",
          reverse: true,
          className: "raa_structure"
        },
        componentParts
      )
    );
  };

  return RoboArmComponents;
}(React.Component);

var RoboArmComponentFeatures = function (_React$Component2) {
  _inherits(RoboArmComponentFeatures, _React$Component2);

  function RoboArmComponentFeatures() {
    _classCallCheck(this, RoboArmComponentFeatures);

    return _possibleConstructorReturn(this, _React$Component2.apply(this, arguments));
  }

  RoboArmComponentFeatures.prototype.render = function render() {
    var _this4 = this;

    // const featureRemove = "all";
    var componentName = this.props.componentName;
    var featureKeys = Object.keys(this.props.featureConfig);
    /* let displayFeatureKeys = featureKeys.filter(
      feature => feature.indexOf(featureRemove) < 0
    ); */
    var featureParts = featureKeys.map(function (featureName) {
      return React.createElement(Topology.Part, {
        id: componentName + "-" + featureName,
        status: "ok",
        label: featureName,
        direction: "row",
        demarcate: false,
        justify: "start",
        align: "center",
        key: featureName,
        onClick: _this4.props.onClick,
        className: "raa_feature",
        reverse: true,
        name: "componentfeature"
      });
    });
    return React.createElement(
      Topology.Parts,
      { direction: "column", uniform: true },
      featureParts
    );
  };

  return RoboArmComponentFeatures;
}(React.Component);

var RoboArmControlFeatures = function (_React$Component3) {
  _inherits(RoboArmControlFeatures, _React$Component3);

  function RoboArmControlFeatures() {
    _classCallCheck(this, RoboArmControlFeatures);

    return _possibleConstructorReturn(this, _React$Component3.apply(this, arguments));
  }

  RoboArmControlFeatures.prototype.render = function render() {
    var _this6 = this;

    var featureDisplay = "all";
    var featureKeys = Object.keys(this.props.featureConfig);
    // console.log(featureKeys.length == 1);
    var displayFeatureKeys = [];
    if (featureKeys.length == 1) {
      displayFeatureKeys = featureKeys;
    } else {
      displayFeatureKeys = featureKeys.filter(function (feature) {
        return feature.indexOf(featureDisplay) > -1;
      });
    }
    // console.log(displayFeatureKeys);
    var featureParts = displayFeatureKeys.map(function (featureName) {
      return React.createElement(
        Topology.Part,
        {
          id: featureName,
          direction: "column",
          demarcate: false,
          justify: "start",
          align: "start",
          key: featureName
        },
        React.createElement(RoboArmControlFeatureActions, {
          actionConfig: _this6.props.featureConfig[featureName].actions,
          featureName: featureName,
          controlName: _this6.props.controlName,
          onClick: _this6.props.onClick
        })
      );
    });
    return React.createElement(
      Topology.Parts,
      { direction: "column", uniform: true },
      featureParts
    );
  };

  return RoboArmControlFeatures;
}(React.Component);

var RoboArmControlFeatureActions = function (_React$Component4) {
  _inherits(RoboArmControlFeatureActions, _React$Component4);

  function RoboArmControlFeatureActions() {
    _classCallCheck(this, RoboArmControlFeatureActions);

    return _possibleConstructorReturn(this, _React$Component4.apply(this, arguments));
  }

  RoboArmControlFeatureActions.prototype.render = function render() {
    var _this8 = this;

    var featureName = this.props.featureName;
    var controlName = this.props.controlName;
    var actionKeys = Object.keys(this.props.actionConfig);
    var actionParts = actionKeys.map(function (actionName) {
      return React.createElement(Topology.Part, {
        id: controlName + "-" + actionName,
        status: "ok",
        label: actionName,
        direction: "row",
        demarcate: false,
        justify: "start",
        align: "center",
        key: featureName + "-" + actionName,
        onClick: _this8.props.onClick,
        className: "raa_action",
        name: "componentaction"
      });
    });
    return React.createElement(
      Topology.Parts,
      { direction: "column", uniform: true },
      actionParts
    );
  };

  return RoboArmControlFeatureActions;
}(React.Component);

var RoboArmApp = function (_React$Component5) {
  _inherits(RoboArmApp, _React$Component5);

  function RoboArmApp(props) {
    _classCallCheck(this, RoboArmApp);

    var _this9 = _possibleConstructorReturn(this, _React$Component5.call(this, props));

    _this9.handle_mode_switch = function (event) {
      console.log(event.target.value);
    };

    _this9.command_click = function (event) {
      var clicked_componentfeature = undefined,
          clicked_componentaction = undefined,
          cl_parts = undefined,
          cl_links = undefined;

      cl_parts = _this9.state.clicked_items;

      if (event.target.parentElement.getAttribute("name") == "componentfeature") {
        clicked_componentfeature = event.target.parentNode.id.split("-");
        cl_parts[0].component = clicked_componentfeature[0];
        cl_parts[0].feature = clicked_componentfeature[1];
        // console.log("clicked a feature: " + cl_parts[0].feature);
      } else {
          clicked_componentaction = event.target.parentNode.id.split("-");
          cl_parts[1].component = clicked_componentaction[0];
          cl_parts[1].action = clicked_componentaction[1];
          // console.log("clicked a action: " + cl_parts[1].action);
        }

      /* hacky bit of hardcoding to make the interface a bit nicer */
      if (cl_parts[1].component == "light") {
        cl_parts[0].component = "light";
        cl_parts[0].feature = "switch";
      }

      if (cl_parts[1].component == "base") {
        cl_parts[0].component = "base";
        cl_parts[0].feature = "direction";
      }

      if (cl_parts[0].component == cl_parts[1].component && cl_parts[0].component != "") {
        _this9.update_links(cl_parts[0].component, cl_parts[0].feature, cl_parts[1].action);

        cl_parts[1].component = "";
      }

      _this9.setState({
        clicked_items: cl_parts
      });
    };

    _this9.state = {
      move_command: { arm: 0, base: 0, light: 0 },
      clicked_items: CLICKED_ITEMS,
      command_links: LINKS
    };
    return _this9;
  }

  RoboArmApp.prototype.update_links = function update_links(component, feature, action) {
    var updated_link = false;
    var curr_links = this.state.command_links;

    for (var i = 0; i < curr_links.length; i++) {
      // console.log("checking: " + i);
      // console.log("component: " + links[i].component);
      // console.log("feature: " + links[i].feature);
      if (curr_links[i].component == component && curr_links[i].feature == feature) {
        curr_links[i].ids = [component + "-" + feature, component + "-" + action];
        updated_link = true;
        // console.log("updating: " + i);
      }
    }
    if (!updated_link) {
      curr_links.push({
        colorIndex: "graph-3",
        ids: [component + "-" + feature, component + "-" + action],
        component: component,
        feature: feature
      });
    }

    this.setState({
      command_links: curr_links
    });

    this.invoke_api(component, feature, action);
  };

  RoboArmApp.prototype.invoke_api = function invoke_api(component, feature, action) {
    var api_url = window.location.protocol + "//" + window.location.hostname + ":" + window.location.port;
    var api_path = "roboarm/" + component + "/" + feature + "/" + action;

    console.log(api_url + api_path);

    var raa = this;

    fetch(api_url + "/" + api_path).then(function (resp) {
      return resp.json();
    }).then(function (data) {
      raa.update_move_command(data);
    }).catch(function (error) {
      console.log("ERROR: " + error);
    });
  };

  RoboArmApp.prototype.update_move_command = function update_move_command(move_command_response) {
    this.setState({
      move_command: move_command_response
    });
  };

  RoboArmApp.prototype.render = function render() {
    return React.createElement(
      App,
      null,
      React.createElement(
        Box,
        {
          align: "center",
          pad: "medium",
          colorIndex: "neutral-1",
          margin: "medium",
          pad: "small",
          direction: "column"
        },
        React.createElement(
          Box,
          { margin: "medium" },
          React.createElement(CheckBox, {
            label: "Live Mode",
            id: "mode_switch",
            name: "mode_switch",
            defaultChecked: true,
            onChange: this.handle_mode_switch,
            disabled: true
          })
        ),
        React.createElement(
          Box,
          { margin: "medium" },
          React.createElement("img", { src: window.location.protocol + "//" + window.location.hostname + ":8081", alt: "Live Feed" })
        ),
        React.createElement(
          Box,
          { margin: "medium" },
          React.createElement(
            Topology,
            {
              a11yTitle: this.props.roboarmConfig.description,
              links: this.state.command_links
            },
            React.createElement(
              Topology.Parts,
              { direction: "column", uniform: true },
              React.createElement(
                Topology.Part,
                { direction: "column" },
                React.createElement(RoboArmComponents, {
                  componentConfig: this.props.roboarmConfig.components,
                  roboArmName: this.props.roboarmConfig.description,
                  onClick: this.command_click
                })
              )
            )
          )
        )
      )
    );
  };

  return RoboArmApp;
}(React.Component);

var element = document.getElementById("content");
ReactDOM.render(React.createElement(RoboArmApp, { roboarmConfig: ROBOARM }), element);
