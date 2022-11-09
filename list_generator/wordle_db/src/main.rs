use std::io;
use std::vec::Vec;
use serde::{Deserialize, Serialize};
use serde_json::{Result, Value};
use std::fs::File;
use std::io::Write;


#[derive(Clone, Debug, Deserialize, Serialize)]
struct Row {
    date: String,
    number: u32,
    word: String,
    url: String,
    epoch: i64,
}

// Depecrated
/*fn example() -> Vec<Row> {
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
}*/

/*fn get_by_date(rows: &Vec<Row>, date: &str) -> Row {
    for row in rows {
        if row.date == date {
            return row.clone();
        }
    }

    panic!("No row found for date {}", date);
}*/

/*fn get_today(rows: &Vec<Row>) -> Row {
    let today = chrono::Local::today().format("%Y-%m-%d").to_string();
    return get_by_date(rows, &today);
}*/

fn get_row_from_json_str(json_str: &str) -> Result<Row> {
    let v: Value = serde_json::from_str(json_str)?;
    let date = v["print_date"].as_str().unwrap().to_string();
    let number = v["days_since_launch"].as_u64().unwrap() as u32;
    let word = v["solution"].as_str().unwrap().to_string();
    let mut url = "https://www.nytimes.com/svc/wordle/v2/".to_owned();
    url.push_str(date.clone().as_str());
    url.push_str(".json");

    let parsed_date = chrono::NaiveDate::parse_from_str(date.as_str(), "%Y-%m-%d").unwrap();
    let epoch = parsed_date.and_hms(8, 0, 0).timestamp();

    return Ok(Row {
        date: date,
        number: number,
        word: word,
        url: url,
        epoch: epoch,
    });
}

fn output_vec_to_json(rows: &Vec<Row>, filename: &str) {
    let mut file = std::fs::File::create(filename).unwrap();
    let json = serde_json::to_string_pretty(rows).unwrap();
    file.write_all(json.as_bytes()).unwrap();
}

async fn fill_vec(row_vec: &mut Vec<Row>) {
    let mut curr_date = chrono::Local::today();
    let curr_epoch = curr_date.and_hms(0, 0, 0).timestamp();
    println!("Current epoch: {}", curr_epoch);

    loop {
        let curr_date_str = curr_date.format("%Y-%m-%d").to_string();
        let url = format!("https://www.nytimes.com/svc/wordle/v2/{curr_date_str}.json");
        let response = reqwest::get(url).await.unwrap();

        if !response.status().is_success() {
            if response.status().as_u16() == 404 {
                println!("404 for {}", curr_date_str);
                break;
            } else {
                // We are likely being ratelimited, wait a couple of seconds
                println!("Ratelimited, waiting 2 seconds...");
                std::thread::sleep(std::time::Duration::from_secs(2));
                println!("Resumed...");
                continue;
            }
        }

        println!("Got status code {} for {}.", response.status().as_u16(), curr_date_str);

        let text = response.text().await.unwrap();
        let row = get_row_from_json_str(&text).unwrap();

        row_vec.push(row);
        //println!("{:?}", row_vec.last().unwrap());
        curr_date += chrono::Duration::days(1);
    }
}

fn output_to_js(rows: &Vec<Row>, filename: &str) {
    let mut file = std::fs::File::create(filename).unwrap();
    let mut js = "let answerList = ".to_owned();
    let json = serde_json::to_string_pretty(rows).unwrap();
    js.push_str(json.as_str());
    file.write_all(js.as_bytes()).unwrap();
}

fn get_vec_from_json(filename: &str) -> Vec<Row> {
    let file = File::open(filename).unwrap();
    let reader = std::io::BufReader::new(file);
    let rows: Vec<Row> = serde_json::from_reader(reader).unwrap();

    return rows;
}

#[tokio::main]
async fn main() {
    // let mut row_vec: Vec<Row> = Vec::new();
    // fill_vec(&mut row_vec).await;
    // output_vec_to_json(&row_vec, "output.json");

    let row_vec = get_vec_from_json("output.json");
    output_to_js(&row_vec, "answerList.js");
}
