package com.narabhut.autopi;

import java.io.DataOutputStream;
import java.util.ArrayList;

import android.os.AsyncTask;
import android.util.Log;

public class OutputGPIOTask extends AsyncTask<Void,Void,Void> {
	
	DataOutputStream out = null;
	int pinNumber = -99;
	int state = 0;
	ArrayList<Integer> validPins = null;
	
	public OutputGPIOTask(int pinNumber, DataOutputStream out, int state){
		this.pinNumber = pinNumber;
		this.out = out;
		this.state = state;
		validPins = new ArrayList<Integer>(8);
		validPins.add(4);
		validPins.add(18);
	}
	@Override
	protected Void doInBackground(Void... params) {
		if (!validPins.contains(pinNumber)){
			return null;
		}
		try {
			if (pinNumber>9){
				out.writeUTF("1"+pinNumber+state);
				Log.e("narabhut","1"+pinNumber+state);
			}
			else{
				out.writeUTF("10"+pinNumber+state);
				Log.e("narabhut","10"+pinNumber+state);
			}
		} catch (Exception e){
			e.printStackTrace();
		}
		return null;
	}

}
