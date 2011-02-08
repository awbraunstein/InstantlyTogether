//
//  FreeFriendsViewController.h
//  oAuth2Test
//
//  Created by Andrew Braunstein on 1/15/11.
//  Copyright 2011 UPenn. All rights reserved.
//

#import <UIKit/UIKit.h>

@interface FreeFriendsViewController : UIViewController
	<UITableViewDelegate, UITableViewDataSource>
{

	NSMutableArray *_listData;
	UITableView* _table;
	NSMutableArray *_names;
	NSMutableArray *_ids;
	NSMutableArray *_times;
	
	UILabel *switchLabel;
	UISwitch *toggleSwitch;
	
}

@property(nonatomic, retain) IBOutlet UITableView* table;
@property(nonatomic, retain) NSMutableArray *listData;
@property(nonatomic, retain) NSMutableArray *names;
@property(nonatomic, retain) NSMutableArray *ids;
@property(nonatomic, retain) NSMutableArray *times;

@property (nonatomic,retain) IBOutlet UILabel *switchLabel;
@property (nonatomic,retain) IBOutlet UISwitch *toggleSwitch;


-(IBAction) switchValueChanged;
-(IBAction) toggleButtonPressed;

@end
