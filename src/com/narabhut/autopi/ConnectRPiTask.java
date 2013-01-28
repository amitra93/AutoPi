package com.narabhut.autopi;

import java.net.Socket;
import android.os.AsyncTask;

public class ConnectRPiTask extends AsyncTask<Void,Void,Socket> {
	
	String IPADDRESS = "24.13.207.78";
	int PORT = 23476;
	Socket connection = null;
	
	@Override
	protected Socket doInBackground(Void... params) {
		try {
			connection = new Socket(IPADDRESS,PORT);
		} catch (Exception e){
			e.printStackTrace();
		}
		return connection;
	}

}
