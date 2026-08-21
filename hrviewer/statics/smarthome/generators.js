// Python generators for the custom blocks. Everything is emitted as top-level
// statements calling the injected `sh` facade; hat-like blocks (schedule/on/
// setTimeout) wrap their body in a generated def and register it. Built-in
// blocks fall back to pythonGenerator's own generators.
(function () {
  "use strict";

  var P = Blockly.Python;
  var UNIT_SECONDS = { ms: 0.001, s: 1, sec: 1, min: 60, h: 3600 };

  function reg(name, fn) {
    if (P.forBlock) P.forBlock[name] = fn;
    else P[name] = fn;
  }
  function fnName(prefix, block) {
    return prefix + block.id.replace(/[^A-Za-z0-9_]/g, "_");
  }
  function body(gen, block, name) {
    return gen.statementToCode(block, name) || gen.INDENT + "pass\n";
  }

  reg("comment", function (block) {
    return "# " + (block.getFieldValue("COMMENT") || "") + "\n";
  });

  reg("schedule", function (block, gen) {
    gen = gen || P;
    var fn = fnName("_sched_", block);
    return (
      "def " + fn + "():\n" + body(gen, block, "STATEMENT") +
      "sh.schedule(" + gen.quote_(block.getFieldValue("SCHEDULE")) + ", " + fn + ")\n"
    );
  });

  reg("on", function (block, gen) {
    gen = gen || P;
    var fn = fnName("_on_", block);
    return (
      "def " + fn + "():\n" + body(gen, block, "STATEMENT") +
      "sh.on(" + gen.quote_(block.getFieldValue("OID")) + ", " +
      gen.quote_(block.getFieldValue("CONDITION")) + ", " + fn + ")\n"
    );
  });

  reg("debug", function (block, gen) {
    gen = gen || P;
    var text = gen.valueToCode(block, "TEXT", gen.ORDER_NONE) || "''";
    return "sh.debug(" + text + ", " + gen.quote_(block.getFieldValue("Severity")) + ")\n";
  });

  reg("control", function (block, gen) {
    gen = gen || P;
    var val = gen.valueToCode(block, "VALUE", gen.ORDER_NONE) || "None";
    return "sh.control(" + gen.quote_(block.getFieldValue("OID")) + ", " + val + ")\n";
  });

  reg("get_value", function (block, gen) {
    gen = gen || P;
    var code =
      "sh.get_value(" + gen.quote_(block.getFieldValue("OID")) + ", " +
      gen.quote_(block.getFieldValue("ATTR")) + ")";
    return [code, gen.ORDER_FUNCTION_CALL];
  });

  reg("time_get", function (block, gen) {
    gen = gen || P;
    return ["sh.time(" + gen.quote_(block.getFieldValue("OPTION")) + ")", gen.ORDER_FUNCTION_CALL];
  });

  reg("timeouts_settimeout", function (block, gen) {
    gen = gen || P;
    var delay = Number(block.getFieldValue("DELAY")) || 0;
    var unit = block.getFieldValue("UNIT");
    var secs = delay * (UNIT_SECONDS[unit] || 0.001);
    var fn = fnName("_to_", block);
    return (
      "def " + fn + "():\n" + body(gen, block, "STATEMENT") +
      "sh.set_timeout(" + gen.quote_(block.getFieldValue("NAME")) + ", " + secs + ", " + fn + ")\n"
    );
  });

  reg("timeouts_cleartimeout", function (block, gen) {
    gen = gen || P;
    return "sh.clear_timeout(" + gen.quote_(block.getFieldValue("NAME")) + ")\n";
  });
})();
