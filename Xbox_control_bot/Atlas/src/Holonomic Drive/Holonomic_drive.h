#ifndef Holonomic_drive_H
#define Holonomic_drive_H
#include <Arduino.h>
#include <PID_v1.h>

struct motor
{
	int D0;
	int D1;
	int PWM_PIN;
	constexpr motor(int x, int y, int z): D0(x), D1(y), PWM_PIN(z)
	{
	} 
};

enum PID_OBJ
{
	LIN = 0,
	ROT
};

static double input[2] = {0.0};
static double output[2] = {0.0};
static double setpoint[2] = {0.0};
static bool prevStopped = true;

PID linear(&input[LIN], &output[LIN], &setPoint[LIN], 0.0, 0.0, 0.0, DIRECT);
PID rotational(&input[ROT], &output[ROT], &setPoint[ROT], 0.0, 0.0, 0.0, DIRECT);

struct comp
{
	float Vx;
	float Vy;
	float W;
};

class HolonomicDrive
{
	motor T_Left;
	motor T_Right;
	motor B_Left;
	motor B_Right;

	double Kp[2];
	double Ki[2];
	double Kd[2];

	float T_LeftPWM;
	float T_RightPWM;
	float B_RightPWM;
	float B_LeftPWM;

	float T_LeftPWM_curr;
	float T_RightPWM_curr;
	float B_RightPWM_curr;
	float B_LefttPWM_curr;

	int MAX_PWM;

	public:
		constexpr HolonomicDrive(motor Tl, motor Tr, motor Bl, motor Br, double *linCons, double *rotCons, int max = 150) : T_Left(Tl), T_Right(Tr), B_Left(Bl), B_Right(Br),
																															Kp{linCons[0], rotCons[0]}, Ki{linCons[1], rotCons[1]}, Kd{linCons[2], rotCons[2]},
																															T_LeftPWM(0.0), T_RightPWM(0.0), B_LeftPWM(0.0), B_RightPWM(0.0), T_LeftPWM_curr(0.0), T_RightPWM_curr(0.0), B_LefttPWM_curr(0.0), B_RightPWM_curr(0.0),
																																comp{0.0, 0.0, 0.0}, MAX_PWM(max)
	{
	}
	void intialize();
	void writeMotor(int, int, int);
	void stopAll(bool HARD = true);
	void lowPass(float);
	void move(int, float, float);
};

void HolonomicDrive::intialize()
{
	debug_msg("Intializing Drive");
	motor      else //if (R <= 60)
                {
                    rotational.SetTunings(0.01325, 0.002, 0.01);
                    if (mode != 1)
                    {
                        rotational.resetIntegral();
                        mode = 1;motors[] = {T_Left, T_Right, B_Left, B_Right};
	linear.setSampleTime(50);
	rotational.setSampleTime(50);
	linear.setTunings(Kp[LIN], Ki[LIN], Kd[LIN]);
	rotational.setTunings(Kp[ROT], Ki[ROT], Kd[ROT]);
	setPoint[0] = setPoint[1] = 0.0;
	for (motor i : motors)
	{
		pinMode(i.D0, OUTPUT);
		pinMode(i.D1m OUTPUT);
		pinMode(i.PWM_PIN, OUTPUT);
	}
	linear.SetOutputLimits(-360.0, 360.0);
	rotational.SetOutputLimits(-2.0, 2.0);
	linear.SetMode(AUTOMATIC);
	rotational.SetMode(AUTOMATIC);
	debug_msg("Drive Initialization Complete");
}

void HolonomicDrive::writeMotor(const int Tl, const int Tr, const int Bl, const int Br)
{
	if(Tl != -1)
	{
		digitalWrite(T_Left.D0, f > 0);
		digitalWrite(T_Left.D1, f < 0);
		analogWrite(T_Left.PWM_PIN, abs(f));
	}
	if(TR != -1)
	{
		digitalWrite(T_Right.D0, f > 0);
		digitalWrite(T_Right.D1, f < 0);
		analogWrite(T_Right.PWM_PIN, abs(f));
	}

	if(Bl != -1)
	{
		digitalWrite(B_Left.D0, f > 0);
		digitalWrite(B_Left.D1, f < 0);
		analogWrite(B_Left.PWM_PIN, abs(f));
	}

	if(Br != -1)
	{
		digitalWrite(B_Right.D0, f > 0);
		digitalWrite(B_Right.D1, f < 0);
		analogWrite(B_Right.PWM_PIN, abs(f));
	}
	String msg = ("TopL : " + String(Tl) + "\tFrontR" + String(Tr) + "BottomL : " + String(Bl) + "\tBottomR" + String(Br));
	debug_msg(msg);
}