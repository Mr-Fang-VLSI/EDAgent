# RTL Testcase Workflow

## Choose The Right Functional Block

Prefer blocks with real protocol/datapath meaning over toy arithmetic:
- good first choices: `UART`, `AES`, `SPI`, `DMA sub-block`, `router`, `crossbar`, `stream/FIFO controller`,
- avoid full SoC tops for first-pass clean testcase work,
- avoid blocks whose normal implementation assumes SRAM or large hard macros.

When several candidates exist, optimize for:
1. no macro dependency,
2. manageable dependency closure,
3. enough control/state/datapath structure to stress placement/CTS,
4. reasonable runtime.

## Build Dependency Closure

Package only the minimum RTL set:
- top module,
- direct RTL dependencies,
- required include files.

Do not pull whole repositories into the testcase package when a small dependency closure is enough.

## Default Recommendation For First Clean Testcase

For first-pass no-macro physical-design diagnosis, prefer a communication/control block such as:
- AXI-stream UART,
- small AES core,
- protocol bridge without embedded SRAM.

These are realistic, synthesizable, and easier to reason about than CPU tops.
