package com.example.solarsol;

import android.content.Intent;
import android.icu.util.Calendar;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.util.MonthDisplayHelper;




public class Main2Activity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main2);

        //intent to open this activity
        Intent intent=getIntent();

    }
    public void showCalendar(View view){
        //Calendar cal=Calendar.getInstance();

    }
}
