// Custom block definitions mirroring the IO-Broker Blockly blocks used by the
// exported smarthome script. Field NAMES must match the native XML exactly so
// that a loaded workspace round-trips (comment/schedule/on/debug/control/
// get_value/time_get/timeouts_*). Built-in blocks (controls_if, logic_*, math_
// number, text, procedures_*) are reused as-is.
(function () {
  "use strict";

  Blockly.defineBlocksWithJsonArray([
    {
      type: "comment",
      message0: "// %1",
      args0: [{ type: "field_input", name: "COMMENT", text: "comment" }],
      previousStatement: null,
      nextStatement: null,
      colour: 160,
    },
    {
      type: "schedule",
      message0: "schedule (cron) %1",
      args0: [{ type: "field_input", name: "SCHEDULE", text: "0 0 * * *" }],
      message1: "%1",
      args1: [{ type: "input_statement", name: "STATEMENT" }],
      previousStatement: null,
      nextStatement: null,
      colour: 210,
    },
    {
      type: "on",
      message0: "on change %1 when %2 ack %3",
      args0: [
        { type: "field_input", name: "OID", text: "zigbee2mqtt.0.<device>.state" },
        {
          type: "field_dropdown",
          name: "CONDITION",
          options: [
            ["is true", "true"],
            ["is false", "false"],
            ["any change", "ne"],
            ["any", "any"],
            [">", "gt"],
            [">=", "ge"],
            ["<", "lt"],
            ["<=", "le"],
          ],
        },
        { type: "field_input", name: "ACK_CONDITION", text: "" },
      ],
      message1: "%1",
      args1: [{ type: "input_statement", name: "STATEMENT" }],
      previousStatement: null,
      nextStatement: null,
      colour: 20,
    },
    {
      type: "debug",
      message0: "debug %1 %2",
      args0: [
        {
          type: "field_dropdown",
          name: "Severity",
          options: [
            ["info", "info"],
            ["warn", "warn"],
            ["error", "error"],
            ["debug", "debug"],
          ],
        },
        { type: "input_value", name: "TEXT" },
      ],
      previousStatement: null,
      nextStatement: null,
      colour: 230,
    },
    {
      type: "control",
      message0: "set %1 = %2 with delay %3",
      args0: [
        { type: "field_input", name: "OID", text: "zigbee2mqtt.0.<device>.state" },
        { type: "input_value", name: "VALUE" },
        { type: "field_checkbox", name: "WITH_DELAY", checked: false },
      ],
      previousStatement: null,
      nextStatement: null,
      inputsInline: true,
      colour: 290,
    },
    {
      type: "get_value",
      message0: "value %1 of %2",
      args0: [
        {
          type: "field_dropdown",
          name: "ATTR",
          options: [
            ["value", "val"],
            ["ack", "ack"],
            ["timestamp", "ts"],
            ["last change", "lc"],
          ],
        },
        { type: "field_input", name: "OID", text: "zigbee2mqtt.0.<device>.temperature" },
      ],
      output: null,
      colour: 290,
    },
    {
      type: "time_get",
      message0: "time %1",
      args0: [
        {
          type: "field_dropdown",
          name: "OPTION",
          options: [
            ["weekday (1-7)", "wd"],
            ["hour", "hour"],
            ["minute", "minute"],
            ["second", "second"],
            ["day", "day"],
            ["month", "month"],
            ["year", "year"],
          ],
        },
      ],
      output: "Number",
      colour: 120,
    },
    {
      type: "timeouts_settimeout",
      message0: "setTimeout %1 after %2 %3",
      args0: [
        { type: "field_input", name: "NAME", text: "timer" },
        { type: "field_number", name: "DELAY", value: 60, min: 0 },
        {
          type: "field_dropdown",
          name: "UNIT",
          options: [
            ["ms", "ms"],
            ["s", "s"],
            ["min", "min"],
            ["h", "h"],
          ],
        },
      ],
      message1: "%1",
      args1: [{ type: "input_statement", name: "STATEMENT" }],
      previousStatement: null,
      nextStatement: null,
      colour: 60,
    },
    {
      type: "timeouts_cleartimeout",
      message0: "clearTimeout %1",
      args0: [{ type: "field_input", name: "NAME", text: "timer" }],
      previousStatement: null,
      nextStatement: null,
      colour: 60,
    },
  ]);
})();
