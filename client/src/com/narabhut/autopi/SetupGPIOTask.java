package com.narabhut.autopi;

import java.io.DataOutputStream;
import java.util.ArrayList;

import android.os.AsyncTask;
import android.util.Log;

public class SetupGPIOTask extends AsyncTask<Void,Void,Void> {
	
	DataOutputStream out = null;
	int pinNumber = -99;
	ArrayList<Integer> validPins = null;
	
	public SetupGPIOTask(int pinNumber, DataOutputStream out){
		this.pinNumber = pinNumber;
		this.out = out;
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
				out.writeUTF("0"+pinNumber+"0");
				Log.e("narabhut","0"+pinNumber+"0");
			}
			else{
				out.writeUTF("00"+pinNumber+"0");
				Log.e("narabhut","00"+pinNumber+"0");
			}
		} catch (Exception e){
			e.printStackTrace();
		}
		return null;
	}

}
