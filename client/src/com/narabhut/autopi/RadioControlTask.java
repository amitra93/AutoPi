package com.narabhut.autopi;

import java.io.DataOutputStream;
import java.util.ArrayList;

import android.os.AsyncTask;

public class RadioControlTask extends AsyncTask<Void,Void,Void> {
	
	DataOutputStream out = null;
	int state = -99;
	
	public RadioControlTask(int state, DataOutputStream out){
		this.out = out;
		this.state = state;
	}
	@Override
	protected Void doInBackground(Void... params) {
		try {
			out.writeUTF(state+"000");
		} catch (Exception e){
			e.printStackTrace();
		}
		return null;
	}

}
