package com.narabhut.autopi;

import java.io.DataOutputStream;
import java.io.IOException;
import java.net.Socket;

import android.os.Bundle;
import android.app.Activity;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.view.MenuItem.OnMenuItemClickListener;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.Button;
import android.widget.CompoundButton;
import android.widget.CompoundButton.OnCheckedChangeListener;
import android.widget.RelativeLayout;
import android.widget.Switch;
import android.widget.Toast;

public class MainActivity extends Activity implements OnCheckedChangeListener, OnMenuItemClickListener, OnClickListener{

	String IPADDRESS = "24.13.207.78";
	int PORT = 23476;
	Socket connection = null;
	DataOutputStream out = null;
	Switch gpioPin, gpioPin2;
	RelativeLayout rl;
	boolean playing = true;
	Button buttonPlay, buttonPrev, buttonNext, buttonStop, buttonVolumePlus, buttonVolumeMinus;
	
	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_main);
		try {
			rl = (RelativeLayout) findViewById(R.id.relativeLayout);
			rl.setVisibility(View.INVISIBLE);
			connection = (new ConnectRPiTask()).execute().get();
			if (!connection.isConnected()){
				throw new Exception();
			}
			out = new DataOutputStream(connection.getOutputStream());
			rl.setVisibility(View.VISIBLE);
			
			gpioPin = (Switch)findViewById(R.id.gpioPin);
			gpioPin.setOnCheckedChangeListener(this);
			
			gpioPin2 = (Switch) findViewById(R.id.gpioPin2);
			gpioPin2.setOnCheckedChangeListener(this);
			
			buttonPlay = (Button) findViewById(R.id.buttonPlay);
			buttonPlay.setOnClickListener(this);
			
			buttonPrev = (Button) findViewById(R.id.buttonPrev);
			buttonPrev.setOnClickListener(this);
			
			buttonNext = (Button) findViewById(R.id.buttonNext);
			buttonNext.setOnClickListener(this);
			
			buttonStop = (Button) findViewById(R.id.buttonStop);
			buttonStop.setOnClickListener(this);
			
			buttonVolumePlus = (Button) findViewById(R.id.buttonVolumePlus);
			buttonVolumePlus.setOnClickListener(this);
			
			buttonVolumeMinus = (Button) findViewById(R.id.buttonVolumeMinus);
			buttonVolumeMinus.setOnClickListener(this);
			
			(new SetupGPIOTask(18,out)).execute();
			(new SetupGPIOTask(4,out)).execute();
		}
		catch (Exception e){
			Toast.makeText(getApplicationContext(),"Error connection to IP "+IPADDRESS,Toast.LENGTH_LONG).show();
			e.printStackTrace();	
		}
			
	}
	
	@Override
	public void onCheckedChanged(CompoundButton button, boolean isChecked) {
		if (!connection.isConnected()){
			try {
				connection = (new ConnectRPiTask()).execute().get();
			} catch (Exception e){
				Toast.makeText(getApplicationContext(),"Error connection to IP "+IPADDRESS,Toast.LENGTH_LONG).show();
				e.printStackTrace();	
			}
		}
		if (button.equals(gpioPin)){
			if (isChecked){
				(new OutputGPIOTask(18,out,1)).execute();
			}
			else {
				(new OutputGPIOTask(18,out,0)).execute();
			}
		}
		else if (button.equals(gpioPin2)){
			if (isChecked){
				(new OutputGPIOTask(4,out,1)).execute();
			}
			else {
				(new OutputGPIOTask(4,out,0)).execute();
			}
		}
		
	}
	
	@Override
	public void finish(){
		try {
			out.writeUTF("2222");
			if (!connection.isClosed()) connection.close();
		} catch (IOException e) {
			Log.e("narabhut","Can't close socket/stream");
		}
		
		
	}


	@Override
	public boolean onMenuItemClick(MenuItem item) {
		finish();
		startActivity(getIntent());
		return false;
	}


	@Override
	public void onClick(View v) {
		if (v.equals(buttonNext)){
			(new RadioControlTask(3,out)).execute();
		}
		else if (v.equals(buttonPrev)){
			(new RadioControlTask(4,out)).execute();
		}
		else if (v.equals(buttonPlay)){
			if (playing){
				(new RadioControlTask(9,out)).execute();
				buttonPlay.setText("Play");
			}
			if (!playing){
				(new RadioControlTask(5,out)).execute();
				buttonPlay.setText("Pause");
			}
			playing = !playing;
		}
		else if (v.equals(buttonStop)){
			(new RadioControlTask(6,out)).execute();
			
		}
		else if (v.equals(buttonVolumePlus)){
			(new RadioControlTask(6,out)).execute();
			
		}
		else if (v.equals(buttonVolumeMinus)){
			(new RadioControlTask(8,out)).execute();
			
		}
	}


}
