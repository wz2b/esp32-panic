import esp32
from esp32 import ULP
from machine import mem32
import machine
from esp32_ulp import src_to_binary


source = """\
#define RTC_CNTL_LOW_POWER_ST_REG 0x3FF480C0
#define RTC_CNTL_WAKEUP_STATE_REG 0x3FF48038
#define RTC_CNTL_RDY_FOR_WAKEUP BIT(19)

#############################################################################

entry:
	jump start


#############################################################################
#
# Declare ram usage here if desired
#
#############################################################################


#############################################################################
start:

	MOVE r0, 2000
loop:
	WAIT 40000  // at 8 MHz this is 5 msec, if we do this 1000 times that's 5 seconds
	SUB r0, r0, 1
	jump wake_up, eq
	jump loop

wake_up:
        READ_RTC_FIELD(RTC_CNTL_LOW_POWER_ST_REG, RTC_CNTL_RDY_FOR_WAKEUP)
        AND r0, r0, 1
        JUMP wake_up, eq    // Retry until the bit is set
        WAKE                          // Trigger wake up
        HALT                          // Stop the ULP program

"""


def run():
	binary = src_to_binary(source)
	load_addr, entry_addr = 0, 0

	ulp = ULP()
	ulp.load_binary(load_addr, binary)
	ulp.run(entry_addr)


	esp32.wake_on_ulp(True)

	print("going to sleep")
	machine.deepsleep()


	#
	# We won't ever reach this, because WAKE is going to cause the main
	# processor to reset and start over at the beginning.
	#
	print("I am awake again")


