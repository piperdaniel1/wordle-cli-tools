use std::io;
use std::io::{prelude::*, BufReader};
use std::vec::Vec;
use std::net::{TcpListener, TcpStream};

#[derive(Clone, Debug)]
struct Row {
    date: String,
    number: u32,
    word: String,
    url: String,
}

fn example() -> Vec<Row> {
    // Build the CSV reader and iterate over each record.
    let mut rdr = csv::Reader::from_reader(io::stdin());
    let mut rows: Vec<Row> = Vec::new();

    for result in rdr.records() {
        // The iterator yields Result<StringRecord, Error>, so we check the
        // error here.
        let record = match result {
            Ok(result) => result,
            Err(e) => panic!("error reading CSV: {}", e),
        };

        // Adding to the vector
        rows.push(Row {
            date: record[0].to_string(),
            number: record[1].parse::<u32>().unwrap(),
            word: record[2].to_string(),
            url: record[3].to_string(),
        });
    }

    return rows;
}

fn get_by_date(rows: &Vec<Row>, date: &str) -> Row {
    for row in rows {
        if row.date == date {
            return row.clone();
        }
    }

    panic!("No row found for date {}", date);
}

fn get_today(rows: &Vec<Row>) -> Row {
    let today = chrono::Local::today().format("%Y-%m-%d").to_string();
    return get_by_date(rows, &today);
}

fn handle_connection(mut stream: TcpStream) {
    let buf_reader = BufReader::new(&mut stream);
    let http_request: Vec<_> = buf_reader
        .lines()
        .map(|result| result.unwrap())
        .take_while(|line| !line.is_empty())
        .collect();

    println!("Request: {:#?}", http_request);

    let response = "HTTP/1.1 200 OK\r\n\r\n";
    stream.write(response.as_bytes()).unwrap();
}

fn main() {
    let row_vec = example();

    let sel_row = get_by_date(&row_vec, "2022-11-07");
    let today_row = get_today(&row_vec);

    println!("Selected row: {:?}", sel_row);
    println!("Today's row: {:?}", today_row);

    let listener = TcpListener::bind("127.0.0.1:8080").unwrap();
    
    for stream in listener.incoming() {
        let stream = stream.unwrap();
        println!("Connection established!");
        handle_connection(stream);
    }
}
